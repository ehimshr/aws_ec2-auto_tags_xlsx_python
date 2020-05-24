import boto3
import xlrd
import os
import sys
import logging
import argparse

#Create and configure logger 
#logging.basicConfig(filename="newfile.log", format='%(asctime)s %(message)s', filemode='w') #example
#logging.basicConfig(level=logging.info)
logging.basicConfig(level=logging.INFO)
 
#Create and Object
logger = logging.getLogger(__name__)


## Function to get value of tag key using row_index and col_index
## Read row_list i.e instances list
## Read col_list i.e column list of tags

def tag_value (row_key, col_key, row_list, col_list, sheet):
    row_index = row_list.index(row_key)
    #print("The row index of " + row_key + ":", row_index)

    col_index = col_list.index(col_key)
    #print("The col index of " + col_key + ":", col_index)

    data = [[sheet.cell_value(r,c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
    value = data[row_index][col_index]
    #print("Value:", value)
    return value



def main(arguments):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--excel_path', type=str, required=True, help="File path location for Tags and values data")
    
    args = parser.parse_args(arguments)
    excel_path=args.excel_path

    print('excel_path:',excel_path)
    
    ## To create client for boto3
    ec2 = boto3.resource('ec2')
    client = boto3.client('ec2', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key= os.environ['AWS_SECRET_ACCESS_KEY'], region_name='us-east-1')
    #client = boto3.client('ec2', aws_access_key_id='B*********A', aws_secret_access_key="a*********5", region_name='us-east-1')


    ec2_list = []

    ## To save instances in list from AWS account
    for instance in ec2.instances.all():
        ec2_list.append(instance.id)
    print(ec2_list)

    # To read read excel file
    print("Starting read file ")
    #file_location = "/home/ubuntu/pythn-learn/excel.xlsx"
    file_location = excel_path
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
                value = tag_value(row_key= instance.id, col_key= key, row_list= row_list, col_list= col_list, sheet= sheet)
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


if __name__=='__main__':
    sys.exit(main(sys.argv[1:]))
