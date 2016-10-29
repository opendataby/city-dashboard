import csv
import os

from new import cursor_wrap, dump, timing


@timing
@cursor_wrap
def main(cursor):
    sql = """
        SELECT 'n', obj.osm_id, obj.name, obj.tags->'amenity' AS amenity,
               city.tags->'name' AS city, dist.tags->'name' AS dist, obj.tags->'addr:street', obj.tags->'addr:housenumber',
               ST_X(ST_Centroid(obj.way)), ST_Y(ST_Centroid(obj.way))
        FROM osm_point obj
        LEFT JOIN osm_polygon dist ON ST_Intersects(dist.way, obj.way)
        LEFT JOIN osm_polygon city ON ST_Intersects(city.way, dist.way)
        WHERE city.osm_id = -59195
        AND dist.tags->'boundary'='administrative'
        AND dist.tags->'admin_level'='9'
        AND obj.tags->'amenity' IN (
            'cafe', 'fast_food', 'restaurant',
            'kindergarten', 'school', 'college', 'university',
            'hospital', 'pharmacy'
        )

        UNION

        SELECT 'l', obj.osm_id, obj.name, obj.tags->'amenity',
               city.tags->'name', dist.tags->'name', obj.tags->'addr:street', obj.tags->'addr:housenumber',
               ST_X(ST_Centroid(obj.way)), ST_Y(ST_Centroid(obj.way))
        FROM osm_line obj
        LEFT JOIN osm_polygon dist ON ST_Intersects(dist.way, obj.way)
        LEFT JOIN osm_polygon city ON ST_Intersects(city.way, dist.way)
        WHERE city.osm_id = -59195
        AND dist.tags->'boundary'='administrative'
        AND dist.tags->'admin_level'='9'
        AND obj.tags->'amenity' IN (
            'cafe', 'fast_food', 'restaurant',
            'kindergarten', 'school', 'college', 'university',
            'hospital', 'pharmacy'
        )

        UNION

        SELECT 'p', obj.osm_id, obj.name, obj.tags->'amenity',
               city.tags->'name', dist.tags->'name', obj.tags->'addr:street', obj.tags->'addr:housenumber',
               ST_X(ST_Centroid(obj.way)), ST_Y(ST_Centroid(obj.way))
        FROM osm_polygon obj
        LEFT JOIN osm_polygon dist ON ST_Intersects(dist.way, obj.way)
        LEFT JOIN osm_polygon city ON ST_Intersects(city.way, dist.way)
        WHERE city.osm_id = -59195
        AND dist.tags->'boundary'='administrative'
        AND dist.tags->'admin_level'='9'
        AND obj.tags->'amenity' IN (
            'cafe', 'fast_food', 'restaurant',
            'kindergarten', 'school', 'college', 'university',
            'hospital', 'pharmacy'
        )
    """

    cursor.execute(sql)
    with open('mensk-amenity.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(['osmid', 'name', 'amenity', 'city', 'district', 'street', 'housenumber', 'lat', 'lon'])
        for t, osm_id, name, type, ac, ad, as_, an, x, y in cursor.fetchall():
            if t == 'n':
                x = 'n{}'.format(osm_id)
            if t == 'l':
                x = 'w{}'.format(osm_id)
            if t == 'p':
                if osm_id > 0:
                    x = 'w{}'.format(osm_id)
                else:
                    x = 'r{}'.format(-osm_id)
            spamwriter.writerow([x, name, type, ac, ad, as_, an, x, y])
            # print('\t', 'n1' if any([nt, ntbe, ntru]) else 'n0', nt, ntbe, ntru)
            # print('\t', 'w1' if any([w, wbe, wru]) else 'w0', w, wbe, wru)
            # print('\t', 'x1' if any([nw, nwbe, nwru]) else 'x0', nw, nwbe, nwru)
            # print('\t\t', osm_id)

    sql = """
        SELECT x.city, x.dist, x.amenity, COUNT(*) FROM ({}) x GROUP BY x.city, x.dist, x.amenity
    """.format(sql)

    cursor.execute(sql)
    with open('mensk-amenities.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(['city', 'district', 'amenity', 'count'])
        for city, dist, amenity, count in cursor.fetchall():
            spamwriter.writerow([city, dist, amenity, count])

    sql = """
        SELECT city.tags->'name', dist.tags->'name', MAX(dist.population),
               ST_Area(ST_Union(ST_Intersection(obj.way, dist.way))::geography), ST_Area(ST_Union(dist.way)::geography)
        FROM osm_polygon obj
        LEFT JOIN osm_polygon dist ON ST_Intersects(dist.way, obj.way)
        LEFT JOIN osm_polygon city ON ST_Intersects(city.way, dist.way)
        WHERE city.osm_id = -59195
        AND dist.tags->'boundary'='administrative'
        AND dist.tags->'admin_level'='9'
        AND (obj.tags->'landuse' = 'forest' OR obj.tags->'natural' = 'wood')
        GROUP BY city.tags->'name', dist.tags->'name'
    """

    cursor.execute(sql)
    with open('mensk-forests.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(['city', 'district', 'population', 'forest_area', 'district_area'])
        for city, dist, population, farea, darea in cursor.fetchall():
            spamwriter.writerow([city, dist, population, farea, darea])

    sql = """
            SELECT 'n', obj.osm_id, obj.name, obj.tags->'amenity' AS amenity,
                   city.tags->'name' AS city, obj.tags->'addr:street', obj.tags->'addr:housenumber',
                   ST_X(ST_Centroid(obj.way)), ST_Y(ST_Centroid(obj.way))
            FROM osm_point obj
            LEFT JOIN osm_polygon city ON ST_Intersects(city.way, obj.way)
            LEFT JOIN osm_polygon country ON ST_Intersects(country.way, city.way)
            WHERE country.osm_id = -59065
            AND city.tags->'place' IN ('city', 'town')
            AND obj.tags->'amenity' IN (
                'cafe', 'fast_food', 'restaurant',
                'kindergarten', 'school', 'college', 'university',
                'hospital', 'pharmacy'
            )
            UNION

            SELECT 'l', obj.osm_id, obj.name, obj.tags->'amenity',
                   city.tags->'name', obj.tags->'addr:street', obj.tags->'addr:housenumber',
                   ST_X(ST_Centroid(obj.way)), ST_Y(ST_Centroid(obj.way))
            FROM osm_line obj
            LEFT JOIN osm_polygon city ON ST_Intersects(city.way, obj.way)
            LEFT JOIN osm_polygon country ON ST_Intersects(country.way, city.way)
            WHERE country.osm_id = -59065
            AND city.tags->'place' IN ('city', 'town')
            AND obj.tags->'amenity' IN (
                'cafe', 'fast_food', 'restaurant',
                'kindergarten', 'school', 'college', 'university',
                'hospital', 'pharmacy'
            )

            UNION

            SELECT 'p', obj.osm_id, obj.name, obj.tags->'amenity',
                   city.tags->'name', obj.tags->'addr:street', obj.tags->'addr:housenumber',
                   ST_X(ST_Centroid(obj.way)), ST_Y(ST_Centroid(obj.way))
            FROM osm_polygon obj
            LEFT JOIN osm_polygon city ON ST_Intersects(city.way, obj.way)
            LEFT JOIN osm_polygon country ON ST_Intersects(country.way, city.way)
            WHERE country.osm_id = -59065
            AND city.tags->'place' IN ('city', 'town')
            AND obj.tags->'amenity' IN (
                'cafe', 'fast_food', 'restaurant',
                'kindergarten', 'school', 'college', 'university',
                'hospital', 'pharmacy'
            )
        """

    cursor.execute(sql)
    with open('belarus-amenity.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(['osmid', 'name', 'amenity', 'city', 'street', 'housenumber', 'lat', 'lon'])
        for t, osm_id, name, type, ac, as_, an, x, y in cursor.fetchall():
            if t == 'n':
                x = 'n{}'.format(osm_id)
            if t == 'l':
                x = 'w{}'.format(osm_id)
            if t == 'p':
                if osm_id > 0:
                    x = 'w{}'.format(osm_id)
                else:
                    x = 'r{}'.format(-osm_id)
            spamwriter.writerow([x, name, type, ac, as_, an, x, y])
            # print('\t', 'n1' if any([nt, ntbe, ntru]) else 'n0', nt, ntbe, ntru)
            # print('\t', 'w1' if any([w, wbe, wru]) else 'w0', w, wbe, wru)
            # print('\t', 'x1' if any([nw, nwbe, nwru]) else 'x0', nw, nwbe, nwru)
            # print('\t\t', osm_id)

    sql = """
            SELECT x.city, x.amenity, COUNT(*) FROM ({}) x GROUP BY x.city, x.amenity
        """.format(sql)

    cursor.execute(sql)
    with open('belarus-amenities.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(['city', 'amenity', 'count'])
        for city, amenity, count in cursor.fetchall():
            spamwriter.writerow([city, amenity, count])

    sql = """
            SELECT city.tags->'name', MAX(city.population),
                   ST_Area(ST_Union(ST_Intersection(obj.way, city.way))::geography), ST_Area(ST_Union(city.way)::geography)
            FROM osm_polygon obj
            LEFT JOIN osm_polygon city ON ST_Intersects(city.way, obj.way)
            LEFT JOIN osm_polygon country ON ST_Intersects(country.way, city.way)
            WHERE country.osm_id = -59065
            AND city.tags->'place' IN ('city', 'town')
            AND (obj.tags->'landuse' = 'forest' OR obj.tags->'natural' = 'wood')
            GROUP BY city.tags->'name'
        """

    cursor.execute(sql)
    with open('belarus-forests.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(['city', 'population', 'forest_area', 'district_area'])
        for city, population, farea, darea in cursor.fetchall():
            spamwriter.writerow([city, population, farea, darea])


if __name__ == '__main__':
    main()
