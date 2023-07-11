import couchdb
import argparse
# db = couch["mastadon"]
def create_mastadonidview(db):
    # Define the map function
    map_func = '''
    function(doc) {
        if(doc.id) {
            emit(doc.id, 1)
        };
    }

    '''

    # Save the views to the design document
    design_doc = {
        "_id": "_design/iddesigndoc",
        "language": "javascript",
        "views": {
            "id_map":{
                "map": map_func
            }

        }
    }
    db.save(design_doc)
    print("Saved successfully")
def retrieve_max_mastadonid(db):
    max_result = db.view("iddesigndoc/id_map", descending = True, limit = 1)
    if len(max_result) == 0:
        return -1
    max_id = max_result.rows[0].key
    return max_id
def retrieve_min_mastadonid(db):
    min_result = db.view("iddesigndoc/id_map", descending = False, limit = 1)
    if len(min_result) == 0:
        return -1
    min_id = min_result.rows[0].key
    return min_id
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create id map view for given host")
    parser.add_argument('--ip', required=True, help="IP address for couchdb")
    parser.add_argument('--db', required=True, help="Database name")
    args = parser.parse_args()
    couch = couchdb.Server(f'http://admin:admin@{args.ip}:5984')
    database_name = str(args.db)
    db = couch[database_name]
    create_mastadonidview(db)
