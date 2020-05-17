from fastapi import FastAPI,UploadFile,File
import uvicorn
import csv
import pandas as pd
import re
import json

#init 
app = FastAPI(debug = True)


# Routes
@app.post('/upload')
async def create_upload_file(uploadFile: UploadFile = File(...)):
    contents = uploadFile.file.read().decode()
    test = contents.split(',')
    counter = 0
    info = {}
    info['name'] = []
    info['bmonth'] = []
    info['age'] = []
    # Skip headers
    i = 3
    # Add to information dictionary O(n)
    while i != len(test)-1:
        if counter == 0:
            sub = test[i].replace('\r\n','')
            info['name'].append(sub)
            counter += 1
        elif counter == 1:
            info['bmonth'].append(test[i])
            counter += 1
        elif counter == 2:
            info['age'].append(test[i])
            counter = 0
        i += 1
    result = {}
    # Append to dict based on month O(n)
    for i in range(len(info['bmonth'])):
        if info['bmonth'][i] in result.keys():
            result[info['bmonth'][i]].append({'name':info['name'][i],'age':info['age'][i]})

        else:
            result[info['bmonth'][i]] = [{'name':info['name'][i],'age':info['age'][i]}]
    # Create json file
    with open('result.txt','w') as outfile:
        json.dump(result,outfile)
    return result


if __name__ == '__main__':
    uvicorn.run(app,host = '127.0.0.1',port = '8000')