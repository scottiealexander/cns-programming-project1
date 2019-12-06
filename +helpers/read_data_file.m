function data = read_data_file(filepath)
    fid = fopen(filepath, 'r');
    try
        len = fread(fid, 1, 'int64');
        data = fread(fid, len, 'float64');
    catch me
        fclose(fid);
        rethrow(me);
    end
    fclose(fid);
end
