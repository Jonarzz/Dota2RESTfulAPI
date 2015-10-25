from flask import jsonify, request, Blueprint, abort
from database import heroes

__author__ = 'Jonarzz'

int_keys = ['base_str', 'base_agg', 'base_int', 'movement_speed', 'day_sight_range', 'night_sight_range', 'range']
float_keys = ['turn_rate', 'str_gain', 'agg_gain', 'int_gain', 'base_armor', 'base_att_time']

heroes_route = Blueprint('heroes_route', __name__, template_folder='templates')


@heroes_route.route('/v1/heroes/<int:hero_id>', methods=['GET'])
def get_hero_by_id(hero_id):
    hero = [hero for hero in heroes if hero['id'] == hero_id]
    if len(hero) == 0:
        abort(404)
    return jsonify({'hero' : hero})


@heroes_route.route('/v1/heroes/', methods=['GET'])
def route():
    hero_list = heroes

    if request.args.get('name') is not None:
        hero_name = str(request.args.get('name'))
        hero_list = [hero for hero in hero_list if hero['name'].lower() == hero_name.lower()]

    if request.args.get('dota_name') is not None:
        hero_dota_name = str(request.args.get('dota_name'))
        hero_list = [hero for hero in hero_list if hero_dota_name.lower() in hero['dota_name'].lower()]

    if request.args.get('primary_stats') is not None:
        primary_stats = str(request.args.get('primary_stats'))
        hero_list = [hero for hero in hero_list if primary_stats.lower() in hero['primary_stats'].lower()]

    if request.args.get('role') is not None:
        role = str(request.args.get('role'))
        hero_list = [hero for hero in hero_list if role.lower() in (hero_role.lower() for hero_role in hero['role'])]

    if request.args.get('attack_type') is not None:
        attack_type = str(request.args.get('attack_type'))
        hero_list = [hero for hero in hero_list if attack_type.lower() in hero['attack_type'].lower()]

    for query_name in int_keys:
        if request.args.get(query_name) is not None:
            hero_list = handle_int_filtering(query_name, hero_list, str(request.args.get(query_name)))

    for query_name in float_keys:
        if request.args.get(query_name) is not None:
            hero_list = handle_float_filtering(query_name, hero_list, str(request.args.get(query_name)))

    if len(hero_list) == 0:
        abort(404)

    return jsonify({'heroes' : hero_list})


def handle_int_filtering(query_name, hero_list, query):
    try:
        if query[:3] == 'gte':
            value = int(query[4:])
            hero_list = [hero for hero in hero_list if hero[query_name] >= value]
            return hero_list

        if query[:3] == 'lte':
            value = int(query[4:])
            hero_list = [hero for hero in hero_list if hero[query_name] <= value]
            return hero_list

        if query[:2] == 'gt':
            value = int(query[3:])
            hero_list = [hero for hero in hero_list if hero[query_name] > value]
            return hero_list

        if query[:2] == 'lt':
            value = int(query[3:])
            hero_list = [hero for hero in hero_list if hero[query_name] < value]
            return hero_list

        hero_list = [hero for hero in hero_list if hero[query_name] == int(query)]
        return hero_list
    except ValueError:
        abort(400)


def handle_float_filtering(query_name, hero_list, query):
    if query[:3] == 'gte':
        value = float(query[4:])
        hero_list = [hero for hero in hero_list if hero[query_name] >= value]
        return hero_list

    if query[:3] == 'lte':
        value = float(query[4:])
        hero_list = [hero for hero in hero_list if hero[query_name] <= value]
        return hero_list

    if query[:2] == 'gt':
        value = float(query[3:])
        hero_list = [hero for hero in hero_list if hero[query_name] > value]
        return hero_list

    if query[:2] == 'lt':
        value = float(query[3:])
        hero_list = [hero for hero in hero_list if hero[query_name] < value]
        return hero_list

    hero_list = [hero for hero in hero_list if hero[query_name] == float(query)]
    return hero_list
