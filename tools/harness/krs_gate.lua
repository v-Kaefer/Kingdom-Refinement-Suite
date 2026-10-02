-- KRS gate: compares every row a module patch file contains with what the running game reports.
-- KRS.gate_rows  = { {table=, keys={{col,value},...}, want={col=value,...}, label=} ... }   (generated from the modules)
-- KRS.gate_consts = { {key=, want=} ... }                                                    (rpg_param rows)
-- A check passes as soon as the table is loaded and the row matches. Tables of the level (perk, buff ...) are not loaded
-- at the main menu, so their checks stay pending until the player stage calls KRS.gate("player").

KRS.gate_state = KRS.gate_state or { done = {}, pass = 0, fail = 0 }

local function norm(v)
    if v == nil then return "" end
    return tostring(v)
end

local function same(got, want)
    got, want = norm(got), norm(want)
    if got == want then return true end
    -- an empty cell in the patch file is reported by the database as nil, 0, -1 or an all-zero uuid
    if want == "" then
        return got == "0" or got == "-1" or got == "false" or got == "00000000-0000-0000-0000-000000000000"
    end
    local a, b = tonumber(got), tonumber(want)
    if a and b then return math.abs(a - b) <= 1e-4 * math.max(1, math.abs(b)) end
    return got:lower() == want:lower()
end

local function gate_log(msg) System.LogAlways("KRS_GATE " .. msg) end

function KRS.gate(stage)
    local S = KRS.gate_state
    local cache = {}
    local function table_info(t)
        if cache[t] == nil then
            local ok, info = pcall(Database.GetTableInfo, t)
            if ok and info and info.LineCount and info.LineCount > 0 then
                local cols = {}
                for k = 0, info.ColumnCount - 1 do cols[Database.GetColumnInfo(t, k).Name] = k end
                cache[t] = { info = info, cols = cols, data = {} }
            else
                cache[t] = false
            end
        end
        return cache[t]
    end
    local function column(t, name)
        local c = table_info(t)
        if c.data[name] == nil then c.data[name] = Database.GetTableColumnData(t, c.cols[name]) or false end
        return c.data[name]
    end

    local pending = 0
    for i, chk in ipairs(KRS.gate_rows or {}) do
        if not S.done[i] then
            local t = table_info(chk.table)
            if not t then
                pending = pending + 1
            else
                local found
                local first = chk.keys[1]
                local kd = t.cols[first[1]] and column(chk.table, first[1])
                if kd then
                    for r = 1, #kd do
                        if same(kd[r], first[2]) then
                            local match = true
                            for k = 2, #chk.keys do
                                local col = column(chk.table, chk.keys[k][1])
                                if not (col and same(col[r], chk.keys[k][2])) then match = false break end
                            end
                            if match then found = r break end
                        end
                    end
                end
                S.done[i] = true
                if not found then
                    S.fail = S.fail + 1
                    gate_log("ROW FAIL " .. chk.label .. " :: row not found in table " .. chk.table .. " (stage " .. stage .. ")")
                else
                    local bad = {}
                    for col, want in pairs(chk.want) do
                        local data = t.cols[col] and column(chk.table, col)
                        local got = data and data[found]
                        if not same(got, want) then bad[#bad + 1] = col .. "=" .. norm(got) .. " (want " .. want .. ")" end
                    end
                    if #bad == 0 then
                        S.pass = S.pass + 1
                        gate_log("ROW OK " .. chk.label)
                    else
                        S.fail = S.fail + 1
                        gate_log("ROW FAIL " .. chk.label .. " :: " .. table.concat(bad, ", "))
                    end
                end
            end
        end
    end

    for i, chk in ipairs(KRS.gate_consts or {}) do
        local id = "c" .. i
        if not S.done[id] then
            S.done[id] = true
            local ok, got = pcall(function() return RPG[chk.key] end)
            if ok and same(got, chk.want) then
                S.pass = S.pass + 1
                gate_log("CONST OK " .. chk.key .. " = " .. norm(got))
            else
                S.fail = S.fail + 1
                gate_log("CONST FAIL " .. chk.key .. " = " .. norm(got) .. " (want " .. chk.want .. ")")
            end
        end
    end
    gate_log("STAGE " .. stage .. " pass=" .. S.pass .. " fail=" .. S.fail .. " pending=" .. pending)
end
