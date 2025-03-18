from src.utils import read_index_conf

index_conf = read_index_conf()
CHROM_DB_COLLECTION = index_conf["chrome_db_collection"]
DB_PATH = index_conf["db_path"]

# Model Settings
EMBEDDING_MODEL =  index_conf['embed_model']