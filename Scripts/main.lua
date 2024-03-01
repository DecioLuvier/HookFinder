local function has_value (tab, val)
    for index, value in ipairs(tab) do
        if value == val then
            return true
        end
    end
    return false
end

LoopAsync(1000, function()
    classes = require("Config/WatchClasses")
    ignored = require("Config/IgnoreHooks")
    for i = 1, #classes do
        local classTable = require("Hooks/" .. classes[i])
        for j = 1, #classTable do
            if not has_value(ignored, classTable[j]) then
                if StaticFindObject(classTable[j]):IsValid() then
                    RegisterHook(classTable[j], function(self)
                        print(classTable[j])
                    end)
                end
            end
        end
    end
    return true
end)