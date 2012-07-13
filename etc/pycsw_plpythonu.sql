
CREATE OR REPLACE FUNCTION query_spatial(bbox_data_wkt text, bbox_input_wkt text, predicate text, distance text)
    RETURNS text
AS $$
    from pycsw import util
    return util.query_spatial(bbox_data_wkt, bbox_input_wkt, predicate, distance)
$$ LANGUAGE plpythonu;

CREATE OR REPLACE FUNCTION update_xpath(xml text, recprops text)
    RETURNS text
AS $$
    from pycsw import util
    return util.update_xpath(xml, recprops)
$$ LANGUAGE plpythonu;
