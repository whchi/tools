local json = require "json"
function shuffle(paths)
    local j, k
    local n = #paths

    for i = 1, n do
      j, k = math.random(n), math.random(n)
      paths[j], paths[k] = paths[k], paths[j]
    end

    return paths
end

function load_request_objects_from_file(file)
    local data = {}
    local content

    -- Check if the file exists
    -- Resource: http://stackoverflow.com/a/4991602/325852
    local f=io.open(file,"r")
    if f~=nil then
      content = f:read("*all")

      io.close(f)
    else
      -- Return the empty array
      return lines
    end
    -- Translate Lua value to/from JSON
    data = json.decode(content)

    return shuffle(data)
end

requests = load_request_objects_from_file("./sample.json")

if #requests <= 0 then
    print("multiplerequests: No requests found.")
    os.exit()
end

print("multiplerequests: Found " .. #requests .. " requests")

counter = 1

request = function()
    -- Get the next requests array element
    local request_object = requests[counter]
    -- Increment the counter
    counter = counter + 1

    -- If the counter is longer than the requests array length then reset it
    if counter > #requests then
        counter = 1
    end
    -- Return the request object with the current URL path
    return wrk.format(request_object.method, request_object.path, {["Content-Type"] = "application/json"}, json.encode(request_object.body))
end
logfile = io.open("wrk.log", "w");
response = function(status, headers, body)
    if status ~= 200 then
        logfile:write("status:" .. status .. ", header:" .. headers['Content-Type'] .. "\n");
    end
end
