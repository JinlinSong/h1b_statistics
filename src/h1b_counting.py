'''
Python Version: Python 3.6.1 :: Anaconda custom (x86_64)
'''

import sys
class H1B_CSV_dataset:
    def __init__(self, data_file, sep = ';'):
        self.value = True
        self.data_input = []
        try:
            with open(data_file,'r',encoding="utf-8") as f:
                for row in f:
                    self.data_input.append(row.strip('\n').split(sep))
        except:
            print('Error: Not able to load data from given input file.')
            self.value = False
            sys.exit()
            
    ### csv validation method
    def is_valid(self):
        return self.value
    
    ### get H1B CSV dataset header
    def data_header(self):
        return self.data_input[0] if self.value else None
    
    ### get H1B CSV dataset without header
    def data_set(self):
        return self.data_input[1:] if self.value else None

def extract_related_columns(data_set, data_header, state_column_name = 'WORKSITE_STATE',
                            occupation_column_name = 'SOC_NAME',
                            status_column_name = 'CASE_STATUS'):
    
    related_column_index = []
    try:
        state_index = data_header.index(state_column_name)
        related_column_index.append(state_index)
    except:
        print('Error: Not able to find state_column_name, please specify correct state_column_name.')
        return False
    try:
        occupation_index = data_header.index(occupation_column_name)
        related_column_index.append(occupation_index)
    except:
        print('Error: Not able to find occupation_column_name, please specify correct occupation_column_name.')
        return False
    try:
        status_index = data_header.index(status_column_name)
        related_column_index.append(status_index)
    except:
        print('Error: Not able to find status_column_name, please specify correct status_column_name.')
        return False
    
    ### extract related columns
    H1B_dataset = [[e[i].strip('"') for i in related_column_index] for e in data_set]
    
    ### remove non-certified records
    H1B_dataset_certified = [e[:2] for e in H1B_dataset if e[2] == 'CERTIFIED']
    
    return H1B_dataset_certified

 class H1B_stat:
    def __init__(self, H1B_dataset_certified):
        self.H1B_dataset_certified = H1B_dataset_certified
        self.total_records = len(H1B_dataset_certified)

    def occupation_stat(self):
        occupation_stat_dict = {}
        for record in self.H1B_dataset_certified:
            if record[1] in occupation_stat_dict:
                occupation_stat_dict[record[1]] += 1
            else:
                occupation_stat_dict[record[1]] = 1
        
        ### sort occupation_stat_dict
        occupation_stat_set = sorted(occupation_stat_dict.items(), key = lambda kv: kv[1], reverse = True)[:10]

        ### add percentaga    
        occupation_stat_set = [[e[0], e[1], float(round(100*e[1]/self.total_records, 1))] for e in occupation_stat_set]    

        return occupation_stat_set
    
    def state_stat(self):
        state_stat_dict = {}
        for record in self.H1B_dataset_certified:
            if record[0] in state_stat_dict:
                state_stat_dict[record[0]] += 1
            else:
                state_stat_dict[record[0]] = 1
                
        ### sort state_stat_dict
        state_stat_set = sorted(state_stat_dict.items(), key = lambda kv: kv[1], reverse = True)[:10]

        ### add percentaga    
        state_stat_set = [[e[0], e[1], float(round(100*e[1]/self.total_records, 1))] for e in state_stat_set]    

        return state_stat_set

def write_data(dataset, path, data_type):
    file_header = "NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE"
    with open(path, 'w') as f:
        if data_type == 'TOP_OCCUPATIONS':
            file_header = "TOP_OCCUPATIONS;" + file_header
        elif data_type == 'TOP_STATES':
            file_header = "TOP_STATES;" + file_header
        else:
            print("Error: Invalid data_type, please specify data_type as 'TOP_OCCUPATIONS' or 'TOP_STATES'.")
            return False
        
        ### write header to the output file
        f.write(file_header + '\n')
        
        ### convert integer to string
        dataset_output = [[e[0], str(e[1]), str(e[2]) + '%'] for e in dataset]
        
        ### write data to the output file
        for item in dataset_output:
            f.write(";".join(item) + '\n')
    return True

def main():

    ### get input path and out_put path
    if len(sys.argv) != 4:
        print('Please specify Four parameters: h1b_counting.py, input path, top_10_occupations path and top_10_states path!')
        return False

    else:    
        input_path = sys.argv[1]
        top_10_occupations_path = sys.argv[2]
        top_10_states_path = sys.argv[3]

    ### specify state_column_name, occupation_column_name, and status_column_name
	state_column_name, occupation_column_name, status_column_name = 'WORKSITE_STATE','SOC_NAME', 'CASE_STATUS'


    ### Process H1B CSV dataset in csv file, getting related columns of certified H1B data
    H1B_CSV_dataset = H1B_CSV_dataset(input_path, sep = ';')
    data_header = H1B_CSV_dataset.data_header()
	data_set = H1B_CSV_dataset.data_set()
	H1B_dataset_certified = extract_related_columns(data_set, data_header, state_column_name,occupation_column_name, status_column_name)

	### Process certified H1B data to get top_10_occupations and top_10_states
	H1B_stat = H1B_stat(H1B_dataset_certified)
	state_stat = H1B_stat.state_stat()
	occupation_stat = H1B_stat.occupation_stat()

	### Write data to top_10_occupations, and top_10_states file
	write_data(state_stat, top_10_states_path, data_type = 'TOP_STATES')
	write_data(occupation_stat, top_10_occupations_path, data_type = 'TOP_OCCUPATIONS')
    return True

if __name__ == '__main__':
    main()




