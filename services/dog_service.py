from bson import json_util, ObjectId
from infrastructure.mongo import mongo
from errors.error_handlers import *
from models.dog_model import Dog

# Method to create a dog
def create_dog_service():
    dog_data = request.get_json()

    name = dog_data.get('name'),
    gender = dog_data.get('gender'),
    size = dog_data.get('size'),
    weight = dog_data.get('weight'),
    birth_date = dog_data.get('birth_date'),
    adopted = dog_data.get('adopted', False),

    if name and gender and size and weight and birth_date and adopted:
        new_dog = Dog(name, gender, size, weight, birth_date, adopted)

        response = mongo.db.dogs.insert_one(new_dog.to_dict())
        result = jsonify({
            'id': str(response.inserted_id),
            **new_dog.to_dict()
        })
        return result
    else:
        return bad_request()

# Method to get all dogs
def get_all_dogs_service():
    dog_data = list(mongo.db.dogs.find())
    result = json_util.dumps(dog_data)
    return result

# Method to get a dog by its id
def get_dog_by_id_service(id):
    print(id)

    # Find the dog by ObjectId
    dog_data = mongo.db.dogs.find_one({'_id': ObjectId(id)})

    # Serialize the data using json_util to handle ObjectId
    result = json_util.dumps(dog_data)

    return result

# Method to search dogs through various ways
def get_dogs_by_data_service(page=1, limit=10):
    # Get query parameters
    query_params = request.args.to_dict()

    # Build a filter dictionary
    filter = {}
    if 'name' in query_params:
        filter['name'] = query_params['name']
    if 'gender' in query_params:
        filter['gender'] = query_params['gender']
    if 'size' in query_params:
        filter['size'] = query_params['size']
    if 'birth_date' in query_params:
        filter['birth_date'] = query_params['birth_date']

    # Calculate pagination
    skip = (page - 1) * limit
    total = mongo.db.dogs.count_documents(filter)

    # Find dogs
    dog_data = mongo.db.dogs.find(filter).skip(skip).limit(limit)

    # Convert dog_data to a list of dictionaries
    formatted_data = []
    for dog in dog_data:
        # Convert _id ObjectId to string and include all fields
        dog["_id"] = str(dog["_id"])
        formatted_data.append(dog)

    result = {
        "message": "Retrieved from database",
        "total": total,
        "page": page,
        "limit": limit,
        "data": formatted_data
    }

    return result

# Method to delete dog
def delete_dog_by_id_service(id):
    dog_data = mongo.db.dogs.delete_one({'_id': ObjectId(id)})
    if dog_data.deleted_count == 1:
        return success('Dog' + id + 'deleted successfully')
    else:
        return not_found()

# Method to fully update dog
def update_dog_by_id_service(id):
    dog_data = mongo.db.dogs.find_one({'_id': ObjectId(id)})
    if dog_data:
        dog_data['name'] = request.get_json()['name']
        dog_data['gender'] = request.get_json()['gender']
        dog_data['size'] = request.get_json()['size']
        dog_data['weight'] = request.get_json()['weight']
        dog_data['birth_date'] = request.get_json()['birth_date']
        dog_data['adopted'] = request.get_json()['adopted']

        result = mongo.db.dogs.update_one({'_id': ObjectId(id)}, {'$set': dog_data})
        if result.modified_count == 1:
            return success('Dog' + id + 'updated successfully')
        else:
            return bad_request()

    else:
        return not_found()


# Method to change dog status into 'adopted'
def update_dog_adopted_service(id):
    dog_data = mongo.db.dogs.find_one({'_id': ObjectId(id)})
    if dog_data:
        dog_data['adopted'] = True
        result = mongo.db.dogs.update_one({'_id': ObjectId(id)}, {'$set': dog_data})
        if result.modified_count == 1:
            return success('Dog' + id + 'updated successfully')
        else:
            return bad_request()
    else:
        return not_found()

# Method to partially update a dog
def update_dog_data_service(id):
    # Obtain dog from db
    dog_data = mongo.db.dogs.find_one({'_id': ObjectId(id)})
    if not dog_data:
        return not_found()

    # Get JSON data from the request
    update_data = request.get_json()

    # Create a dictionary
    fields_to_update = {}

    # Check for each field in the update
    if 'name' in update_data:
        fields_to_update['name'] = update_data['name']
    if 'gender' in update_data:
        fields_to_update['gender'] = update_data['gender']
    if 'size' in update_data:
        fields_to_update['size'] = update_data['size']
    if 'weight' in update_data:
        fields_to_update['weight'] = update_data['weight']
    if 'birth_date' in update_data:
        fields_to_update['birth_date'] = update_data['birth_date']
    if 'adopted' in update_data:
        fields_to_update['adopted'] = update_data['adopted']

    # If there are fields to update, perform the update
    if fields_to_update:
        result = mongo.db.dogs.update_one({'_id': ObjectId(id)}, {'$set': fields_to_update})
        if result.modified_count == 1:
            return success(f'Dog {id} updated successfully')
        else:
            return bad_request('No changes were made')
    else:
        return bad_request('No fields provided to update')
