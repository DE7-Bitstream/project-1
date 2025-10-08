import os
import csv
import pandas as pd

def get_csv_full_path(file_name):
    csv_dir = os.path.join(os.getcwd() , 'csv')
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)
    if file_name[-4:] != '.csv':
        file_name += '.csv'
    csv_file_path = os.path.join(csv_dir, file_name)
    return csv_file_path



def write_data_to_csv(file_name, data):
    
    csv_file_path = get_csv_full_path(file_name)

    # 딕셔너리의 키를 필드 이름(헤더)으로 사용
    fieldnames = data[0].keys()
    try:
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            # DictWriter 객체 생성
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # 헤더(필드 이름) 쓰기
            writer.writeheader()
            # 데이터를 한 줄씩 쓰기
            writer.writerows(data)
        print(f"✅ 성공적으로 저장: {csv_file_path}")
    except Exception as e:
        raise Exception(f"❌ 파일 저장 중 오류 발생: {e}")



def get_column_unique_data(file_name, column_names):

    csv_file_path = get_csv_full_path(file_name)
    
    try:
        df = pd.read_csv(csv_file_path, encoding='utf-8')

        # 단일 컬럼일 경우
        if isinstance(column_names, str):
            unique_values = df[column_names].unique().tolist()
        # 다중 컬럼일 경우
        else:
            unique_combinations_df = df[column_names].drop_duplicates()
            unique_values = [tuple(row) for row in unique_combinations_df.values.tolist()]
        return unique_values
    
    except FileNotFoundError:
        raise FileNotFoundError(f"❌ 오류: '{csv_file_path}' 파일을 찾을 수 없습니다. 경로를 확인해 주세요.")
    except Exception as e:
        raise Exception(f"❌ CSV 파일을 읽어오는 중 오류가 발생했습니다: {e}")
    


def extract_unique_ids_from_piped_data(file_name, columns_name):

    unique_id_set = set()

    csv_file_path = get_csv_full_path(file_name)
    try:
        df = pd.read_csv(csv_file_path, encoding='utf-8')
        for column in columns_name:
            series = df[column].astype(str).str.strip()
            split_data = series.str.split("|")
            exploded_ids = split_data.explode()
            valid_ids = exploded_ids[(exploded_ids != '')].str.strip()
            unique_id_set.update(valid_ids.unique())
        return unique_id_set
    
    except FileNotFoundError:
        raise FileNotFoundError(f"❌ 오류: '{csv_file_path}' 파일을 찾을 수 없습니다. 경로를 확인해 주세요.")
    except Exception as e:
        raise Exception(f"❌ CSV 파일을 읽어오는 중 오류가 발생했습니다: {e}")
    
