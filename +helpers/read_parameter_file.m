function d = read_parameter_file(filepath)
    d = jsondecode(fileread(filepath));
end
