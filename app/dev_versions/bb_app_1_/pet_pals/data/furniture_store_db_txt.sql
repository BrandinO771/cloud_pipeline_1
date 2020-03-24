BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "orders_list" (
	"Order_Date"	TEXT,
	"Order_id"	TEXT,
	"Customer_id"	TEXT,
	"Item_Code"	TEXT,
	"Quantity"	INTEGER,
	"Item_Name"	TEXT,
	"Item_Category"	TEXT,
	"Type"	TEXT,
	"Style"	TEXT,
	"Seating_Material"	TEXT,
	"Frame"	TEXT
);
CREATE TABLE IF NOT EXISTS "customer_list" (
	"First_Name"	TEXT,
	"Last_Name"	TEXT,
	"Gender"	TEXT,
	"Birth_Year"	INTEGER,
	"Customer_id"	TEXT UNIQUE,
	"Street"	TEXT,
	"City"	TEXT,
	"State"	TEXT,
	"Zip"	INTEGER,
	"Phone"	TEXT,
	PRIMARY KEY("Customer_id")
);
INSERT INTO "orders_list" VALUES ('2020-02-03','O_64937','C_50136','cch_6',1,'Lovers','couch','sleeper','Modern','canvas','wood');
INSERT INTO "orders_list" VALUES ('2020-02-20','O_77348','C_62728','cch_2',2,'Couchy_McCouchster','couch','love','Rustic','vinyl','wood');
INSERT INTO "orders_list" VALUES ('2020-02-01','O_32930','C_41410','stl_1',6,'Stool_Pigeon','stool','tall_backless','Urban','leather','aluminum');
INSERT INTO "orders_list" VALUES ('2020-02-16','O_32930','C_41410','cch_7',2,'Dealers_Lounge','couch','sectional','Modern','leather','wood');
INSERT INTO "orders_list" VALUES ('2020-02-15','O_65925','C_20973','cch_7',1,'Dealers_Lounge','couch','love','Urban','vinyl','wood');
INSERT INTO "orders_list" VALUES ('2020-02-12','O_66248','C_23298','cha_4',2,'The_Executive','chair','captain','Rustic','suede','wood');
INSERT INTO "orders_list" VALUES ('2020-02-19','O_76504','C_32164','stl_5',4,'Tooshy_Zone','stool','tall_low_back_arms','Modern','leather','wood');
INSERT INTO "orders_list" VALUES ('2020-02-16','O_76504','C_32164','stl_1',1,'Stool_Pigeon','stool','tall_low_back','Modern','canvas','aluminum');
INSERT INTO "orders_list" VALUES ('2020-02-17','O_83115','C_41114','stl_4',8,'Booty_Scooty','stool','tall_low_back','Rustic','suede','aluminum');
INSERT INTO "orders_list" VALUES ('2020-02-09','O_83115','C_41114','cch_6',1,'Lovers','couch','long','Rustic','vinyl','wood');
INSERT INTO "orders_list" VALUES ('2020-02-18','O_86342','C_85289','cch_5',1,'Den_Master','couch','long','Modern','leather','wood');
INSERT INTO "orders_list" VALUES ('2020-02-01','O_91478','C_70214','cch_5',1,'Den_Master','couch','sectional','Modern','microfiber','wood');
INSERT INTO "orders_list" VALUES ('2020-02-01','O_91478','C_70214','cha_4',6,'The_Executive','chair','table','Designer','suede','wood');
INSERT INTO "orders_list" VALUES ('2020-02-17','O_62918','C_67302','stl_1',4,'Stool_Pigeon','stool','tall_backless','Designer','vinyl','steel');
INSERT INTO "customer_list" VALUES ('Fay','McCoy','female',1978,'C_64143','1004 Maple Parkway','Steamy River','CO',96904,'441-555-2337');
INSERT INTO "customer_list" VALUES ('Sabrina','McFadden','female',1970,'C_17237','1609 Star Light Parkway','Sleepy Springs','NM',88854,'555-555-1365');
INSERT INTO "customer_list" VALUES ('Wendy','Pinkerton','female',1974,'C_23298','1449 Ocean View Ave','Copper Rock','MT',72651,'685-555-3583');
INSERT INTO "customer_list" VALUES ('Alaina','ColeBottom','female',1959,'C_87704','762 Cedar Blvd','Sleepy Mine','UT',64584,'345-555-2341');
INSERT INTO "customer_list" VALUES ('Alma','Scott','female',1964,'C_70560','1127 Elm Ave','Lost Creek','CA',84036,'642-555-5268');
INSERT INTO "customer_list" VALUES ('Sasha','Zanderman','female',1963,'C_62728','586 First Ave','Gold Mills','NV',58854,'709-555-4953');
INSERT INTO "customer_list" VALUES ('Nana','DoLittle','female',1949,'C_41410','1449 Beverly Blvd','Green Meadows','CO',39659,'868-555-3728');
INSERT INTO "customer_list" VALUES ('Unika','UnderHill','female',1956,'C_85289','1875 Gopher Ave','Pleasant Meadows','OR',39875,'870-555-4530');
INSERT INTO "customer_list" VALUES ('Gertrude','FlapperSmith','female',1976,'C_32164','1565 Fox Blvd','Green Ton','ID',89502,'675-555-2269');
INSERT INTO "customer_list" VALUES ('MoonBeam','VonBerg','female',1955,'C_12461','1006 Elm Way','Copper Stream','CO',92246,'767-555-7644');
INSERT INTO "customer_list" VALUES ('Tim','Stein''ErTon','male',1940,'C_67302','943 First Blvd','Little Mine','WA',96702,'660-555-4565');
INSERT INTO "customer_list" VALUES ('Kale','WackerPort','male',1982,'C_70761','1747 Bakers Ave','Gold Springs','CO',46944,'561-555-1335');
INSERT INTO "customer_list" VALUES ('Jet','PoleTon','male',1975,'C_20973','1049 Kings Ave','Pleasant Ville','NV',84189,'729-555-8994');
INSERT INTO "customer_list" VALUES ('Zed','SilverTon','male',1980,'C_13112','1773 School Ave','Nowhere Pond','ID',49540,'777-555-3346');
INSERT INTO "customer_list" VALUES ('Frank','WolfMan','male',1970,'C_50330','775 Cedar Street','Nowhere Mills','AZ',48787,'788-555-6260');
INSERT INTO "customer_list" VALUES ('Herb','RickBlocker','male',1972,'C_70214','1485 Bakers Parkway','Old Rock','AZ',58421,'265-555-6622');
INSERT INTO "customer_list" VALUES ('Zeek','McGillicuddy','male',1941,'C_50136','546 Ocean View Blvd','Dreamy Stream','OR',66874,'840-555-8437');
INSERT INTO "customer_list" VALUES ('Garamond','AppleTree','male',1966,'C_41114','791 Cedar Street','Dreamy River','UT',78613,'347-555-1199');
INSERT INTO "customer_list" VALUES ('Boo','FreeMoon','male',1972,'C_29915','1558 Fox Court','Steamy Ton','CA',85000,'247-555-8433');
INSERT INTO "customer_list" VALUES ('Kay','McPeepers','male',1967,'C_97892','476 Main Road','Pony Ville','CA',53547,'688-555-8947');
CREATE VIEW customers_join_orders AS
SELECT * 
FROM orders_list
LEFT JOIN customer_list
	ON orders_list.Customer_id = customer_list.Customer_id
ORDER BY Order_Date;
COMMIT;
