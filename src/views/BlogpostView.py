from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.BlogpostModel import BlogpostModel, BlogpostSchema

blogpost_api = Blueprint('blogpost_api', __name__)
blogpost_schema = BlogpostSchema()


@blogpost_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    req_data = request.get_json()
    req_data['owner_id'] = g.user.get('id')
    data = blogpost_schema.load(req_data)

    post = BlogpostModel(data)
    post.save()
    data = blogpost_schema.dump(post)
    return custom_response(data, 201)


@blogpost_api.route('/', methods=['GET'])
def get_all():
    posts = BlogpostModel.get_all_blogposts()
    data = blogpost_schema.dump(posts, many=True)
    return custom_response(data, 200)


@blogpost_api.route('/<int:id>', methods=['GET'])
def get_one(id):
    post = BlogpostModel.get_one_blogpost(id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = blogpost_schema.dump(post)
    return custom_response(data, 200)


@blogpost_api.route('/<int:id>', methods=['PUT'])
@Auth.auth_required
def update(id):
    req_data = request.get_json()
    post = BlogpostModel.get_one_blogpost(id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = blogpost_schema.dump(post)
    if data.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    data = blogpost_schema.load(req_data, partial=True)
    post.update(data)

    data = blogpost_schema.dump(post)
    return custom_response(data, 200)

@blogpost_api.route('/<int:id>', methods=['DELETE'])
@Auth.auth_required
def delete(id):
    post = BlogpostModel.get_one(id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = blogpost_schema.dump(post)
    if data.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    post.delete()
    return custom_response({'message': 'deleted'}, 204)




def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )
