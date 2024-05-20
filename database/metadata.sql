SET SEARCH_PATH TO astro_project;

INSERT INTO observer_region (name, latitude, longitude)
VALUES ('East Midlands', 53.2081,-0.4386),
('East of England', 52.3333 ,0.4520),
('Greater London', 51.4171, -0.1433),
('North East England', 54.8400, -1.0400),
('North West England', 53.9900, -3.4600),
('Northern Ireland', 54.5000, -6.9400),
('Scotland', 57.1305, -4.5395),
('South East England', 51.2000, -0.2700),
('South West England', 50.7000, -3.1000),
('Wales', 52.5521, -4.2947),
('West Midlands', 52.5300, -2.1810),
('Yorkshire and the Humber', 54.1341, -0.8107);

INSERT INTO observer_location (name, latitude, longitude, region_id)
VALUES ('Aberdeenshire', 57.1667, -2.6667, 7),
('Angus', 56.6667, -2.9167, 7),
('Antrim', 54.8650, -6.2800, 6),
('Argyllshire', 56.2517, -5.2514, 7),
('Armagh', 54.3499, -6.6546, 6),
('Ayrshire', 55.5000, -4.5000, 7),
('Banffshire', 57.5000, -3.0833, 7),
('Bedfordshire', 52.0627, -0.5292, 2),
('Berkshire', 51.4670, -1.1854, 8),
('Berwickshire', 55.7500, -2.500, 7),
('Blaenau Gwent', 51.7876, -3.2044, 10),
('Bridgend', 51.5043, -3.5769, 10),
('Buckinghamshire', 51.7500, -0.7500, 8),
('Buteshire', 55.7500, -5.2500, 7),
('Caerphilly', 51.5788, -3.2181, 10),
('Caithness', 58.4303, -3.4650, 7),
('Cardiff', 51.4837, -3.1681, 10),
('Carmarthenshire', 51.8572, -4.3116, 10),
('Cambridgeshire', 52.3333, 0.0833, 2),
('Ceredigion', 52.2500, -4.0000, 10),
('Cheshire', 53.2326, -2.6103, 5),
('City of London', 51.5072, -0.1276, 3),
('Clackmannanshire', 56.1664, -3.7514, 7),
('Conwy', 53.2829, -3.8295, 10),
('Cornwall', 50.4167, -4.7500, 9),
('County Durham', 54.6667, -1.7500, 4),
('Cumbria', 54.5772, -2.7975, 5),
('Denbighshire', 53.1842, -3.4225, 10),
('Derbyshire', 53.1667, -1.5833, 1),
('Devon', 50.7500, -3.7500, 9),
('Dorset', 50.7500, -2.3333, 9),
('Down', 54.3289, -5.7159, 6),
('Dumfries and Galloway', 55.0833, -3.8333, 7),
('Dumfriesshire', 55.1667, -3.5000, 7),
('East Ayrshire', 55.5000, -4.2500, 7),
('East Dunbartonshire', 55.9333, -4.2000, 7),
('East Lothian', 55.9158, -2.7512, 7),
('East Riding of Yorkshire', 53.9112, -0.5813, 12),
('East Sussex', 50.9086, 0.2494, 8),
('Essex', 51.5742, 0.4857, 2),
('Fermanagh', 54.3439, -7.6312, 6),
('Fife', 56.3333, -3.0000, 7),
('Flintshire', 53.1669, -3.1419, 10),
('Gloucestershire', 51.8333, -2.1667, 9),
('Greater London', 51.4309, -0.0936, 3),
('Greater Manchester', 53.4576, -2.1578, 5),
('Gwynedd', 52.9277, -4.1335, 10),
('Hampshire', 51.0833, -1.1667, 8),
('Herefordshire', 52.0833, -2.7500, 11),
('Hertfordshire', 51.8098, -0.2377, 2),
('Highland', 57.5066, -5.0038, 7),
('Inverclyde', 55.9000, -4.7500, 7),
('Invernessshire', 57.0833, -4.6667, 7),
('Isle of Anglesey', 53.2500, -4.3333, 10),
('Isle of White', 50.6938, -1.3047, 8),
('Kent', 51.2475, 0.7105, 8),
('Kirkcudbrightshire', 55.0000, -4.0000, 7),
('Lanarkshire', 55.5753, -3.8333, 7),
('Lancashire', 53.7632, -2.7044, 5),
('Leicestershire', 52.6667, -1.0000, 1),
('Lincolnshire', 53.1667, -0.2500, 1),
('Londonderry', 54.9958, -7.3074, 6),
('Merthyr Tydfil', 51.7487, -3.3816, 10),
('Merseyside', 53.3976, -2.9437, 5),
('Mid Glamorgan', 51.5000, -3.4500, 7),
('Midlothian', 55.8333, -3.0833, 7),
('Monmouthshire', 51.7501, -2.8333, 10),
('Moray', 57.4167, -3.2500, 7),
('Neath Port Talbot', 51.6917, -3.7347, 10),
('Newport', 51.5842, -2.9977, 10),
('Norfolk', 52.6667, 1.0000, 2),
('Northamptonshire', 52.2500, -0.8333, 1),
('Northumberland', 55.2500, -2.0006, 4),
('North Yorkshire', 53.9915, -1.5412, 12),
('Nottinghamshire', 53.1003, -0.9936, 1),
('Oxfordshire', 51.8333, -1.2500, 8),
('Pembrokeshire', 51.8340, -4.9167, 10),
('Perth and Kinross', 56.5000, -3.7500, 7),
('Powys', 52.6464, -3.3261, 10),
('Renfrewshire', 55.8333, -4.5000, 7),
('Rhondda Cynon Taf', 51.6490, -3.4289, 10),
('Rutland', 52.6583, -0.6396, 1),
('The Scottish Borders', 55.5833, -2.8333, 7),
('Selkirkshire', 55.5000, -3.0000, 7),
('Shetland Islands', 60.3333, -1.3333, 7),
('Shropshire', 52.7064, -2.7418, 11),
('Somerset', 51.0833, -3.0000, 9),
('South Lanarkshire', 55.5832, -3.8332, 7),
('South Yorkshire', 53.4697, -1.3260, 12),
('Staffordshire', 52.8793, -2.0572, 11),
('Stirlingshire', 56.0701, -3.9087, 7),
('Strathclyde Region', 56.0000, -5.1667, 7),
('Suffolk', 52.1872, 0.9708, 2),
('Surrey', 51.3148, -0.5600, 8),
('Sutherland', 58.2500, -4.5001, 7),
('Swansea', 51.6214, -3.9436, 10),
('Tayside Region', 56.4167, -3.5333, 7),
('Torfaen', 51.7002, -3.0446, 10),
('Tyne and Wear', 54.9167, -1.5667, 4),
('Tyrone', 54.6539, -7.2908, 6),
('The Vale of Glamorgan', 51.4096, -3.4848, 10),
('Warwickshire', 52.2671, -1.4675, 11),
('West Dunbartonshire', 55.9667, -4.5333, 7),
('Western Isles', 57.6667, -7.1667, 7),
('West Glamorgan', 51.5833, -3.7500, 10),
('West Lothian', 55.9167, -3.5000, 7),
('West Midlands', 52.5000, -1.8333, 11),
('West Sussex', 51.0000, -0.4167, 8),
('West Yorkshire', 53.8108, -1.7626, 12),
('Wiltshire', 51.2500, -1.9167, 9),
('Worcestershire', 52.2545, -2.2668, 11),
('Wrexham', 53.0301, -3.0261, 10);

INSERT INTO aurora_status (colour, status)
VALUES ('Green', 'No significant activity'),
('Yellow', 'Minor geomagnetic activity'),
('Amber', 'Amber alert: possible aurora'),
('Red', 'Red alert: aurora likely');


