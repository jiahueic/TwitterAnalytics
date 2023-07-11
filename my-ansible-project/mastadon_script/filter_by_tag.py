import couchdb
import argparse
parser = argparse.ArgumentParser(description="Count Mastadon hashtags")
parser.add_argument('--ip', required=True, help = "IP Address of CouchDb Host")
args = parser.parse_args()
couch = couchdb.Server(f'http://admin:admin@{args.ip}:5984')
db = couch["mastadon"]
def create_tagcountview():
    # Define the map function
    map_func = '''
    function(doc) {
        if (doc.tags) {
            doc.tags.forEach(function(tags){
                if (tags.name) {
                    emit(tags.name, 1)
                }
            });
        }
    }

    '''

    # Define the reduce function 
    reduce_func = '''
    function(keys, values, rereduce) {
        return sum(values);
    }

    '''

    # Save the views to the design document
    design_doc = {
        "_id": "_design/mydesigndoc",
        "views":{
            "tag_count_map":{
                "map": map_func,
                "reduce": reduce_func
            }
        }
    }

    db.save(design_doc)
    print("Saved successfully")

def top_10_hashtag():
    # Query the view and get the tag counts
    query_result = db.view('mydesigndoc/tag_count_map', group = True, reduce = True)
    tag_counts = {}
    for res in query_result:
        if res.key != "mentalhealth":
            tag_counts[res.key] = res.value
    top_10_tags = sorted(tag_counts, key = tag_counts.get, reverse=True)[:10]
    for tag in top_10_tags:
        count = tag_counts[tag]
        print("Hashtag: ", tag, " Counts: ", count)
if __name__ == "__main__":
    create_tagcountview()
