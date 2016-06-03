import csv
import time
import sys

# Prompt to type in file directory
print 'Welcome!\n'
print 'Please confirm the raw data files have been put in the "input_files" folder.(Press Enter to continue)\n'
sys.stdin.readline()

file_name = raw_input('Please type in the file name, without the file extension: ')

# Open file for row counting
print "Opening source file..."
file_dir = 'input_files/'+str(file_name)+'.csv'
csv_file = open(file_dir)
csv_reader = csv.reader(csv_file)

# Count the row
print "Counting the rows..."
data = list(csv_reader)
row_count = len(data)

# Create 2-D list
print "Creating index..."
raw_data = [['' for x in range(24)] for y in range(row_count)]

# Open file for data mapping
print "Mapping data..."
csv_file = open(file_dir)
csv_reader = csv.reader(csv_file)

# Map data to list
row_number = 0
for row in csv_reader:
    for column_count in range(24):
        raw_data[row_number][column_count] = row[column_count]
    row_number += 1

# Change date format
print "Changing date format..."
for row_number in range(row_count):
    from_date = raw_data[row_number][2]
    conv_date = time.strptime(from_date, "%Y%m%d")
    target_date = time.strftime("%d/%m/%Y", conv_date)
    raw_data[row_number][2] = target_date

# Fill blank time space
print "Filling in blank columns for VISIT START & VISITSTOP..."
for row_number in range(row_count):
    if raw_data[row_number][18] == '':
        raw_data[row_number][18] = raw_data[row_number-1][18]
    if raw_data[row_number][19] == '':
        raw_data[row_number][19] = raw_data[row_number-1][19]

# Count EXP
print "Counting expense items"
exp_count_t = 0
exp_count_f = 0
for row_number in range(row_count):
    if raw_data[row_number][17] == 'T':
        exp_count_t += 1
    if raw_data[row_number][17] == 'F':
        exp_count_f += 1

# Create lists for expense items
print "Creating lists for expense items..."
exp_t = [['' for x in range(10)] for y in range(exp_count_t)]
exp_f = [['' for x in range(27)] for y in range(exp_count_f)]

# Map data to expense lists
print "Mapping data..."
row_number_exp_t = 0
row_number_exp_f = 0
for row_number in range(row_count):
    # Expense True List
    if raw_data[row_number][17] == 'T':
        exp_t[row_number_exp_t][0] = 'ACTADDP'                         # Type
        exp_t[row_number_exp_t][1] = raw_data[row_number][0]           # Employee No.
        exp_t[row_number_exp_t][2] = raw_data[row_number][2]           # Day Date
        exp_t[row_number_exp_t][3] = raw_data[row_number][18]          # Start Time
        exp_t[row_number_exp_t][4] = raw_data[row_number][2]           # Trans Date
        exp_t[row_number_exp_t][5] = raw_data[row_number][18]          # Trans Start Time
        exp_t[row_number_exp_t][6] = raw_data[row_number][19]          # Trans Finish Time
        exp_t[row_number_exp_t][7] = raw_data[row_number][6]           # Transaction Type
        exp_t[row_number_exp_t][8] = raw_data[row_number][12]          # Qty
        exp_t[row_number_exp_t][9] = ''                                # Note
        row_number_exp_t += 1

    # Expense False List
    if raw_data[row_number][17] == 'F':
        exp_f[row_number_exp_f][0] = 'ACTUAL'                          # Type
        exp_f[row_number_exp_f][1] = raw_data[row_number][0]           # Employee No.
        exp_f[row_number_exp_f][2] = raw_data[row_number][2]           # Day Date
        exp_f[row_number_exp_f][3] = raw_data[row_number][11]          # Area
        if raw_data[row_number][6] == 'Norm':
            exp_f[row_number_exp_f][4] = 'P99'
        else:
            exp_f[row_number_exp_f][4] = raw_data[row_number][6]     # Shift/Allowance
        if raw_data[row_number][5] == '':
            exp_f[row_number_exp_f][5] = 'Normal'
        else:
            exp_f[row_number_exp_f][5] = raw_data[row_number][5]     # Role ID
        exp_f[row_number_exp_f][6] = raw_data[row_number][18]          # Start Time
        exp_f[row_number_exp_f][7] = raw_data[row_number][19]          # Finish Time
        exp_f[row_number_exp_f][8] = raw_data[row_number][12]          # Work Hrs
        exp_f[row_number_exp_f][9] = '00:00'
        exp_f[row_number_exp_f][10] = '00:00'
        exp_f[row_number_exp_f][11] = 'R'
        exp_f[row_number_exp_f][12] = 'N'
        exp_f[row_number_exp_f][13] = ''
        exp_f[row_number_exp_f][14] = ''
        exp_f[row_number_exp_f][15] = ''
        exp_f[row_number_exp_f][16] = 'N'
        exp_f[row_number_exp_f][17] = 'N'
        exp_f[row_number_exp_f][18] = 'N'
        exp_f[row_number_exp_f][19] = 'N'
        exp_f[row_number_exp_f][20] = 'N'
        exp_f[row_number_exp_f][21] = 'N'
        exp_f[row_number_exp_f][22] = 'N'
        exp_f[row_number_exp_f][23] = 'N'
        exp_f[row_number_exp_f][24] = 'N'
        exp_f[row_number_exp_f][25] = 'N'
        exp_f[row_number_exp_f][26] = 'N'
        row_number_exp_f += 1

# Export final file
print "Exporting..."
output_name = raw_input('Enter the output file name, without file extension: ')+'.csv'
output_dir = 'output_files/'+str(output_name)
csv_file = open(output_dir, 'wb')
csv_file.write('HEADER\n')
csv_file_writerow = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_ALL)
for item in exp_f:
    csv_file_writerow.writerow(item)
for item in exp_t:
    csv_file_writerow.writerow(item)
csv_file_writerow = csv.writer(csv_file, delimiter=',')
# footer = ['FOOTER', row_count]
csv_file.write('FOOTER,'+str(row_count))

result = 'Finish. ' + str(row_count) + ' items have been successfully exported.'
print result
