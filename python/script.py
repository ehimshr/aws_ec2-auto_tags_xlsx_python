import boto3
import xlrd
import os

## To create client for boto3
ec2 = boto3.resource('ec2')
client = boto3.client('ec2', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key= os.environ['AWS_SECRET_ACCESS_KEY'], region_name='us-east-1')

ec2_list = []

## To save instances in list from AWS account
for instance in ec2.instances.all():
    ec2_list.append(instance.id)
print(ec2_list)

# To read read excel file
print("Starting read file ")
file_location = "/home/ubuntu/pythn-learn/excel.xlsx"
workbook = xlrd.open_workbook(file_location)
sheet = workbook.sheet_by_index(0)

## To read rows in excel and put in row_list list
row_list = []
row = 0
while (row in range(sheet.nrows)):
    row_names = sheet.cell_value(row, 0)
    row_list.append(row_names)
    row = row + 1
print('ec2 in row list', row_list)

## To read columns in excel and put in col_list list
col_list = []
col = 0
while (col in range(sheet.ncols)):
    col_names = sheet.cell_value(0, col)
    col_list.append(col_names)
    col = col + 1
print(col_list)

## Funstion to get value of tag key using row_index and col_index
## Read row_list i.e instances list
## Read col_list i.e column list of tags

def tag_value (row_key, col_key):
    row_index = row_list.index(row_key)
    #print("The row index of " + row_key + ":", row_index)

    col_index = col_list.index(col_key)
    #print("The col index of " + col_key + ":", col_index)

    data = [[sheet.cell_value(r,c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
    value = data[row_index][col_index]
    #print("Value:", value)
    return value


for instance in ec2.instances.all():
    if (instance.id in ec2_list):
        print('instance found in list with id', instance.id)
        print('start tagging stage for instance ID:', instance.id)
        #row_key = instance.id
        #A = tag_value(row_key= instance.id, col_key= "A")
        #print("Tag value of A is :", A)
        #tag = ec2.Tag(instance.id, 'A', A)
        col = 1
        while (col in range(sheet.ncols)):
            key = sheet.cell_value(0, col)
            value = tag_value(row_key= instance.id, col_key= key)
            response = client.create_tags(
            Resources=[instance.id],
            Tags = [
                {
                    'Key': key,
                    'Value': value
                }
            ]
            )
            print(response)
            col = col + 1


    else:
        print('instance not found in list with id', instance.id)


