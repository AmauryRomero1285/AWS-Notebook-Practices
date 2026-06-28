import os
import warnings
from pathlib import Path

warnings.simplefilter('ignore')

import pandas as pd
from scipy.io import arff
from sklearn.model_selection import train_test_split

DATA_DIR = Path(__file__).resolve().parent
ARFF_FILE = DATA_DIR / 'column_2C_weka.arff'
ZIP_URL = 'http://archive.ics.uci.edu/ml/machine-learning-databases/00212/vertebral_column_data.zip'
LOCAL_OUTPUT_FILES = {
    'train': DATA_DIR / 'vertebral_train.csv',
    'test': DATA_DIR / 'vertebral_test.csv',
    'validate': DATA_DIR / 'vertebral_validate.csv',
}

USE_AWS = os.environ.get('USE_AWS', 'false').lower() in ('1', 'true', 'yes')


def ensure_arff_file():
    if ARFF_FILE.exists():
        print(f'Found ARFF file: {ARFF_FILE.name}')
        return

    try:
        import requests
        import zipfile
        import io
    except ImportError as exc:
        raise RuntimeError('Missing dependency for downloading data: requests') from exc

    print(f'Downloading dataset from {ZIP_URL}...')
    response = requests.get(ZIP_URL, stream=True)
    response.raise_for_status()
    archive = zipfile.ZipFile(io.BytesIO(response.content))
    archive.extractall(DATA_DIR)
    if not ARFF_FILE.exists():
        raise FileNotFoundError(f'Expected ARFF file not found after download: {ARFF_FILE}')
    print('Downloaded and extracted dataset successfully.')


def load_dataset():
    if not ARFF_FILE.exists():
        ensure_arff_file()

    raw_data = arff.loadarff(str(ARFF_FILE))
    df = pd.DataFrame(raw_data[0])
    return df


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    class_mapper = {b'Abnormal': 1, b'Normal': 0}
    if df['class'].dtype == object or df['class'].dtype == 'bytes':
        df['class'] = df['class'].replace(class_mapper)
    else:
        df['class'] = df['class'].apply(lambda v: class_mapper.get(v, v))

    cols = [c for c in df.columns if c != 'class']
    df = df[['class'] + cols]
    return df


def split_data(df: pd.DataFrame):
    train, test_and_validate = train_test_split(
        df,
        test_size=0.2,
        random_state=42,
        stratify=df['class'],
    )
    test, validate = train_test_split(
        test_and_validate,
        test_size=0.5,
        random_state=42,
        stratify=test_and_validate['class'],
    )
    return train, test, validate


def save_csv(dataframe: pd.DataFrame, filename: Path):
    dataframe.to_csv(filename, header=False, index=False)
    print(f'Wrote {filename.name} ({dataframe.shape[0]} rows, {dataframe.shape[1]} cols)')


def maybe_aws_upload():
    if not USE_AWS:
        print('USE_AWS is disabled. Skipping AWS upload and SageMaker training steps.')
        return

    try:
        import boto3
        import io
    except ImportError as exc:
        print('AWS upload skipped because boto3 is not installed.')
        return

    bucket = 'c215940a5457640l15705140t1w054086190527-labbucket-r2bv51iq2dor'
    prefix = 'lab3'
    s3_resource = boto3.Session().resource('s3')

    def upload_s3_csv(filename: Path, folder: str):
        buffer = io.StringIO()
        dataframe = pd.read_csv(filename, header=None)
        dataframe.to_csv(buffer, header=False, index=False)
        key = os.path.join(prefix, folder, filename.name).replace('\\', '/')
        s3_resource.Bucket(bucket).Object(key).put(Body=buffer.getvalue())
        print(f'Uploaded {filename.name} to s3://{bucket}/{key}')

    upload_s3_csv(LOCAL_OUTPUT_FILES['train'], 'train')
    upload_s3_csv(LOCAL_OUTPUT_FILES['test'], 'test')
    upload_s3_csv(LOCAL_OUTPUT_FILES['validate'], 'validate')


def main():
    print('Running Lab-04 data preparation script...')
    print(f'Working directory: {DATA_DIR}')
    print(f'USE_AWS={USE_AWS}')

    df = load_dataset()
    df = prepare_data(df)

    print('Dataset shape:', df.shape)
    print('Class counts:')
    print(df['class'].value_counts())
    print()

    train, test, validate = split_data(df)
    print('Split sizes: train=%s test=%s validate=%s' % (train.shape, test.shape, validate.shape))
    print('Train class counts:')
    print(train['class'].value_counts())
    print('Test class counts:')
    print(test['class'].value_counts())
    print('Validate class counts:')
    print(validate['class'].value_counts())

    save_csv(train, LOCAL_OUTPUT_FILES['train'])
    save_csv(test, LOCAL_OUTPUT_FILES['test'])
    save_csv(validate, LOCAL_OUTPUT_FILES['validate'])

    maybe_aws_upload()

    print('Lab-04 execution completed successfully.')


if __name__ == '__main__':
    main()
