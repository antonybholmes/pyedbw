-- Login tables

DROP TABLE IF EXISTS persons CASCADE;
CREATE TABLE persons (id SERIAL NOT NULL PRIMARY KEY, 
public_id CHAR(32) NOT NULL UNIQUE,
first_name VARCHAR(255) NOT NULL, 
last_name VARCHAR(255) NOT NULL, 
affiliation VARCHAR(255) NOT NULL, 
phone VARCHAR(255) NOT NULL, 
address VARCHAR(255) NOT NULL, 
email VARCHAR(255) NOT NULL,
password_hash_salted CHAR(128),
salt CHAR(128) NOT NULL,
public_uuid CHAR(32) NOT NULL UNIQUE,
api_key CHAR(64) UNIQUE,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
CREATE INDEX persons_first_name_index ON persons(first_name varchar_pattern_ops);
CREATE INDEX persons_last_name_index ON persons(last_name varchar_pattern_ops);
CREATE INDEX persons_email_index ON persons(email varchar_pattern_ops);
CREATE INDEX persons_public_uuid_index ON persons(public_uuid bpchar_pattern_ops);

DROP TABLE IF EXISTS api_keys CASCADE;
CREATE TABLE api_keys (id SERIAL NOT NULL PRIMARY KEY,
user_id INTEGER NOT NULL UNIQUE, 
public_key varchar(255) NOT NULL UNIQUE,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE api_keys ADD FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE;

DROP TABLE IF EXISTS login_persons CASCADE;
CREATE TABLE login_persons (id SERIAL NOT NULL PRIMARY KEY,
person_id INTEGER NOT NULL UNIQUE, 
user_name VARCHAR(255) NOT NULL UNIQUE, 
password_hash_salted CHAR(128) NOT NULL, 
salt CHAR(128) NOT NULL,
key CHAR(64) NOT NULL UNIQUE,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE login_persons ADD FOREIGN KEY (person_id) REFERENCES persons(id) ON DELETE CASCADE;


DROP TABLE IF EXISTS groups CASCADE;
CREATE TABLE groups (id SERIAL NOT NULL PRIMARY KEY,
name VARCHAR(255) NOT NULL UNIQUE, 
color CHAR(7) NOT NULL DEFAULT '#CCCCCC', 
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
INSERT INTO groups (name) VALUES ('Administrator');
INSERT INTO groups (name) VALUES ('Superuser');
INSERT INTO groups (name) VALUES ('Normal');

DROP TABLE IF EXISTS groups_persons CASCADE;
CREATE TABLE groups_persons (id SERIAL NOT NULL PRIMARY KEY,
group_id INTEGER NOT NULL, 
person_id INTEGER NOT NULL, 
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE groups_persons ADD FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE;
ALTER TABLE groups_persons ADD FOREIGN KEY (person_id) REFERENCES persons(id) ON DELETE CASCADE;
ALTER TABLE groups_persons ADD CONSTRAINT group_person_uq UNIQUE (group_id, person_id);
CREATE INDEX groups_persons_group_id_index ON groups_persons (group_id);
CREATE INDEX groups_persons_persons_id_index ON groups_persons (person_id);


DROP TABLE IF EXISTS groups_samples_persons CASCADE;
CREATE TABLE groups_samples_persons (id SERIAL NOT NULL PRIMARY KEY,
group_id INTEGER NOT NULL, 
person_id INTEGER NOT NULL, 
sample_id INTEGER NOT NULL, 
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE groups_samples_persons ADD FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE;
ALTER TABLE groups_samples_persons ADD FOREIGN KEY (person_id) REFERENCES persons(id) ON DELETE CASCADE;
ALTER TABLE groups_samples_persons ADD FOREIGN KEY (sample_id) REFERENCES samples(id) ON DELETE CASCADE;
ALTER TABLE groups_samples_persons ADD CONSTRAINT group_sample_person_uq UNIQUE (group_id, sample_id, person_id);
CREATE INDEX groups_samples_persons_group_id_index ON groups_samples_persons (group_id);
CREATE INDEX groups_samples_persons_sample_id_index ON groups_samples_persons (sample_id);
CREATE INDEX groups_samples_persons_persons_id_index ON groups_samples_persons (person_id);

-- user tables


DROP TABLE IF EXISTS login_sessions CASCADE;
CREATE TABLE login_sessions (id SERIAL NOT NULL PRIMARY KEY,
key CHAR(64) NOT NULL UNIQUE,
person_id INTEGER NOT NULL UNIQUE,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE login_sessions ADD FOREIGN KEY (person_id) REFERENCES persons(id) ON DELETE CASCADE;


-- Support tables

DROP TABLE IF EXISTS organisms CASCADE;
CREATE TABLE organisms (id SERIAL NOT NULL PRIMARY KEY, 
name varchar(255) NOT NULL UNIQUE,
scientific_name varchar(255) NOT NULL UNIQUE,
tax_id INTEGER NOT NULL,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());

DROP TABLE IF EXISTS providers CASCADE;
CREATE TABLE providers (id SERIAL NOT NULL PRIMARY KEY,
name varchar(255) NOT NULL UNIQUE,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());

DROP TABLE IF EXISTS microarray_assays CASCADE;
CREATE TABLE microarray_assays (id SERIAL NOT NULL PRIMARY KEY, 
name varchar(255) NOT NULL UNIQUE,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());

DROP TABLE IF EXISTS microarray_platforms CASCADE;
CREATE TABLE microarray_platforms (id SERIAL NOT NULL PRIMARY KEY, 
name varchar(255) NOT NULL UNIQUE,
assay_id INTEGER NOT NULL,
provider_id INTEGER NOT NULL,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE microarray_platforms ADD FOREIGN KEY (assay_id) REFERENCES microarray_assays(id) ON DELETE CASCADE;
ALTER TABLE microarray_platforms ADD FOREIGN KEY (provider_id) REFERENCES providers(id) ON DELETE CASCADE;

-- Experiments

DROP TABLE IF EXISTS experiments CASCADE;
CREATE TABLE experiments (id SERIAL NOT NULL PRIMARY KEY,
public_id varchar(255) NOT NULL UNIQUE,
name varchar(255) NOT NULL UNIQUE, 
description TEXT NOT NULL,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());

-- Samples --

DROP TABLE IF EXISTS data_types CASCADE;
CREATE TABLE data_types (id SERIAL NOT NULL PRIMARY KEY, 
name varchar(255) NOT NULL UNIQUE,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());

DROP TABLE IF EXISTS samples CASCADE;
CREATE TABLE samples (id SERIAL NOT NULL PRIMARY KEY,
experiment_id INTEGER NOT NULL,
data_type_id INTEGER NOT NULL,
name varchar(255) NOT NULL,
description varchar(255) NOT NULL DEFAULT '',
organism_id INTEGER NOT NULL,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE samples ADD FOREIGN KEY (experiment_id) REFERENCES experiments(id) ON DELETE CASCADE;
ALTER TABLE samples ADD FOREIGN KEY (organism_id) REFERENCES organisms(id) ON DELETE CASCADE;
ALTER TABLE samples ADD FOREIGN KEY (data_type_id) REFERENCES data_types(id) ON DELETE CASCADE;
CREATE INDEX samples_experiment_id_index ON samples USING btree(experiment_id);
CREATE INDEX samples_expression_type_id_index ON samples USING btree(expression_type_id);
CREATE INDEX samples_organism_id_index ON samples(organism_id);


DROP TABLE IF EXISTS groups_samples CASCADE;
CREATE TABLE groups_samples (id SERIAL NOT NULL PRIMARY KEY,
group_id INTEGER NOT NULL, 
sample_id INTEGER NOT NULL, 
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE groups_samples ADD FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE;
ALTER TABLE groups_samples ADD FOREIGN KEY (sample_id) REFERENCES samples(id) ON DELETE CASCADE;
ALTER TABLE groups_samples ADD CONSTRAINT group_sample_uq UNIQUE (group_id, sample_id);
CREATE INDEX groups_samples_group_id_index ON groups_samples (group_id);
CREATE INDEX groups_samples_persons_id_index ON groups_samples (sample_id);

DROP TABLE IF EXISTS sets CASCADE;
CREATE TABLE sets (id SERIAL NOT NULL PRIMARY KEY, 
name varchar(255) NOT NULL UNIQUE,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());

DROP TABLE IF EXISTS sets_samples CASCADE;
CREATE TABLE sets_samples (id SERIAL NOT NULL PRIMARY KEY,
set_id INTEGER NOT NULL, 
sample_id INTEGER NOT NULL, 
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE sets_samples ADD FOREIGN KEY (set_id) REFERENCES sets(id) ON DELETE CASCADE;
ALTER TABLE sets_samples ADD FOREIGN KEY (sample_id) REFERENCES samples(id) ON DELETE CASCADE;
CREATE INDEX sets_samples_set_id_index ON sets_samples (set_id);
CREATE INDEX sets_samples_persons_id_index ON sets_samples (sample_id);

-- Unfortunately samples can have various names so take account of this --
DROP TABLE IF EXISTS sample_aliases CASCADE;
CREATE TABLE sample_aliases (id SERIAL NOT NULL PRIMARY KEY,
sample_id INTEGER NOT NULL,
name varchar(255) NOT NULL,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE sample_alt_names ADD FOREIGN KEY (sample_id) REFERENCES samples(id) ON DELETE CASCADE;
CREATE INDEX sample_aliases_name_index ON sample_aliases(name varchar_pattern_ops);

DROP TABLE IF EXISTS role CASCADE;
CREATE TABLE role (id SERIAL NOT NULL PRIMARY KEY, 
name varchar(255) NOT NULL UNIQUE);

DROP TABLE IF EXISTS sample_persons CASCADE;
CREATE TABLE sample_persons (id SERIAL NOT NULL PRIMARY KEY,
sample_id INTEGER NOT NULL, 
person_id INTEGER NOT NULL,
role_id INTEGER NOT NULL,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE sample_persons ADD FOREIGN KEY (sample_id) REFERENCES samples(id) ON DELETE CASCADE;
ALTER TABLE sample_persons ADD FOREIGN KEY (person_id) REFERENCES persons(id) ON DELETE CASCADE;
ALTER TABLE sample_persons ADD FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE;
CREATE INDEX sample_persons_person_id_index ON sample_persons(person_id);

--- File System

DROP TABLE IF EXISTS vfs_types CASCADE;
CREATE TABLE vfs_types (id SERIAL NOT NULL PRIMARY KEY, 
name varchar(255) NOT NULL UNIQUE,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
INSERT INTO vfs_types (name) VALUES ('Directory');
INSERT INTO vfs_types (name) VALUES ('File');

DROP TABLE IF EXISTS vfs CASCADE;
CREATE TABLE vfs (id SERIAL NOT NULL PRIMARY KEY,
parent_id INTEGER NOT NULL DEFAULT -1,
name varchar(255) NOT NULL,
type_id INTEGER NOT NULL,
path varchar(255),
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
CREATE INDEX vfs_name_index ON vfs(lower(name) varchar_pattern_ops);
ALTER TABLE vfs ADD FOREIGN KEY (type_id) REFERENCES vfs_types(id) ON DELETE CASCADE;
INSERT INTO vfs (name, type_id) VALUES ('/', 1);
INSERT INTO vfs (name, parent_id, type_id) VALUES ('Experiments', 1, 1);

DROP TABLE IF EXISTS sample_files CASCADE;
CREATE TABLE sample_files (id SERIAL NOT NULL PRIMARY KEY,
sample_id INTEGER NOT NULL,
vfs_id INTEGER NOT NULL,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE sample_files ADD FOREIGN KEY (sample_id) REFERENCES samples(id) ON DELETE CASCADE;
ALTER TABLE sample_files ADD FOREIGN KEY (vfs_id) REFERENCES vfs(id) ON DELETE CASCADE;
ALTER TABLE sample_files ADD CONSTRAINT sample_vfs_unique UNIQUE (sample_id, vfs_id);
CREATE INDEX sample_files_sample_id_index ON sample_files (sample_id);
CREATE INDEX sample_files_vfs_id_index ON sample_files (vfs_id);


DROP TABLE IF EXISTS ucsc_bigbed CASCADE;
CREATE TABLE ucsc_bigbed (id SERIAL NOT NULL PRIMARY KEY,
sample_id INTEGER NOT NULL,
path varchar(255) NOT NULL,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE ucsc_bigbed ADD FOREIGN KEY (sample_id) REFERENCES samples(id) ON DELETE CASCADE;
CREATE INDEX ucsc_bigbed_sample_id_index ON ucsc_bigbed (sample_id);



-- tags

DROP TABLE IF EXISTS tags CASCADE;
CREATE TABLE tags (id SERIAL NOT NULL PRIMARY KEY,
name varchar(255) NOT NULL,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());

DROP TABLE IF EXISTS tag_types CASCADE;
CREATE TABLE tag_types (id SERIAL NOT NULL PRIMARY KEY,
name varchar(255) NOT NULL,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
INSERT INTO tag_types (name) VALUES ('str');
INSERT INTO tag_types (name) VALUES ('int');
INSERT INTO tag_types (name) VALUES ('float');

DROP TABLE IF EXISTS sample_tags CASCADE;
CREATE TABLE sample_tags (id SERIAL NOT NULL PRIMARY KEY,
sample_id INTEGER NOT NULL,
tag_id INTEGER NOT NULL,
tag_type_id INTEGER NOT NULL,
str_value varchar(255),
int_value INTEGER,
float_value FLOAT,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE sample_tags ADD FOREIGN KEY (sample_id) REFERENCES samples(id) ON DELETE CASCADE;
ALTER TABLE sample_tags ADD FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE;
ALTER TABLE sample_tags ADD FOREIGN KEY (tag_type_id) REFERENCES tag_types(id) ON DELETE CASCADE;
CREATE INDEX sample_tags_sample_id_index ON sample_tags (sample_id);
CREATE INDEX sample_tags_tag_id_index ON sample_tags (tag_id);







DROP TABLE IF EXISTS tags_sample CASCADE;
CREATE TABLE tags_sample (id SERIAL NOT NULL PRIMARY KEY,
sample_id INTEGER NOT NULL,
tag_id INTEGER NOT NULL,
value varchar(255) NOT NULL,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE tags_sample ADD FOREIGN KEY (sample_id) REFERENCES samples(id) ON DELETE CASCADE;
ALTER TABLE tags_sample ADD FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE;
CREATE INDEX tags_sample_sample_id_index ON tags_sample (sample_id);
CREATE INDEX tags_sample_tag_id_index ON tags_sample (tag_id);
CREATE INDEX tags_sample_value_index ON tags_sample (value varchar_pattern_ops);


DROP TABLE IF EXISTS sample_tags_json CASCADE;
CREATE TABLE sample_tags_json (id SERIAL NOT NULL PRIMARY KEY,
sample_id INTEGER NOT NULL,
data jsonb NOT NULL,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE sample_tags_json ADD FOREIGN KEY (sample_id) REFERENCES samples(id) ON DELETE CASCADE;
CREATE INDEX sample_tags_json_sample_id_index ON sample_tags_json (sample_id);

-- assign integer numerical data to a sample
DROP TABLE IF EXISTS tags_sample_int CASCADE;
CREATE TABLE tags_sample_int (id SERIAL NOT NULL PRIMARY KEY,
sample_id INTEGER NOT NULL,
tag_id INTEGER NOT NULL, 
value INTEGER NOT NULL,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE tags_sample_int ADD FOREIGN KEY (sample_id) REFERENCES samples(id) ON DELETE CASCADE;
ALTER TABLE tags_sample_int ADD FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE;
CREATE INDEX tags_sample_int_sample_id_index ON tags_sample_int(sample_id);
CREATE INDEX tags_sample_int_tag_id_index ON tags_sample_int(tag_id);
CREATE INDEX tags_sample_int_value_index ON tags_sample_int (value);

DROP TABLE IF EXISTS tags_sample_float CASCADE;
CREATE TABLE tags_sample_float (id SERIAL NOT NULL PRIMARY KEY,
sample_id INTEGER NOT NULL,
tag_id INTEGER NOT NULL, 
value FLOAT NOT NULL,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE tags_sample_float ADD FOREIGN KEY (sample_id) REFERENCES samples(id) ON DELETE CASCADE;
ALTER TABLE tags_sample_float ADD FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE;
CREATE INDEX tags_sample_float_sample_id_index ON tags_sample_float(sample_id);
CREATE INDEX tags_sample_float_tag_id_index ON tags_sample_float(tag_id);
CREATE INDEX tags_sample_float_value_index ON tags_sample_float (value);

DROP TABLE IF EXISTS tags_keywords_search CASCADE;
CREATE TABLE tags_keywords_search (id SERIAL NOT NULL PRIMARY KEY, 
tag_id INTEGER NOT NULL,
keyword_id INTEGER NOT NULL,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE tags_keywords_search ADD CONSTRAINT tag_keyword_unique UNIQUE (tag_id, keyword_id);
ALTER TABLE tags_keywords_search ADD FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE;
ALTER TABLE tags_keywords_search ADD FOREIGN KEY (keyword_id) REFERENCES keywords(id) ON DELETE CASCADE;
CREATE INDEX tags_keywords_search_tag_id_index ON tags_keywords_search(tag_id);
CREATE INDEX tags_keywords_search_keyword_id_index ON tags_keywords_search(keyword_id);

DROP TABLE IF EXISTS tags_samples_search CASCADE;
CREATE TABLE tags_samples_search (id SERIAL NOT NULL PRIMARY KEY,
tag_keyword_search_id INTEGER NOT NULL,
sample_id INTEGER NOT NULL,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE tags_samples_search ADD FOREIGN KEY (tag_keyword_search_id) REFERENCES tags_keywords_search(id) ON DELETE CASCADE;
ALTER TABLE tags_samples_search ADD FOREIGN KEY (sample_id) REFERENCES samples(id) ON DELETE CASCADE;
CREATE INDEX tags_samples_search_tag_keyword_search_id_index ON tags_samples_search(tag_keyword_search_id);


-- tags

-- geo db functions

DROP TABLE IF EXISTS geo_platforms CASCADE;
CREATE TABLE geo_platforms (id SERIAL NOT NULL PRIMARY KEY, 
name varchar(16) NOT NULL UNIQUE,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
CREATE INDEX geo_platforms_name_index ON geo_platforms USING btree(name varchar_pattern_ops);

DROP TABLE IF EXISTS geo_series CASCADE;
CREATE TABLE geo_series (id SERIAL NOT NULL PRIMARY KEY, 
name varchar(16) NOT NULL UNIQUE,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
CREATE INDEX geo_series_name_index ON geo_series USING btree(name varchar_pattern_ops);

DROP TABLE IF EXISTS geo_samples CASCADE;
CREATE TABLE geo_samples (id SERIAL NOT NULL PRIMARY KEY,
geo_series_id INTEGER NOT NULL,
sample_id INTEGER NOT NULL,
geo_platform_id INTEGER NOT NULL,
name varchar(16) NOT NULL UNIQUE,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE geo_samples ADD FOREIGN KEY (geo_series_id) REFERENCES geo_series(id) ON DELETE CASCADE;
ALTER TABLE geo_samples ADD FOREIGN KEY (sample_id) REFERENCES samples(id) ON DELETE CASCADE;
ALTER TABLE geo_samples ADD FOREIGN KEY (geo_platform_id) REFERENCES geo_platforms(id) ON DELETE CASCADE;
CREATE INDEX geo_samples_name_index ON geo_samples USING btree(name varchar_pattern_ops);
CREATE INDEX geo_samples_sample_id_index ON geo_samples USING btree(sample_id);
CREATE INDEX geo_samples_geo_series_id_index ON geo_samples USING btree(geo_series_id);


DROP TABLE IF EXISTS samples_geo CASCADE;
CREATE TABLE samples_geo (id SERIAL NOT NULL PRIMARY KEY,
sample_id INTEGER NOT NULL,
geo_series_accession varchar(16) NOT NULL,
geo_accession varchar(16) NOT NULL UNIQUE,
geo_platform varchar(16) NOT NULL,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE samples_geo ADD FOREIGN KEY (sample_id) REFERENCES samples(id) ON DELETE CASCADE;
CREATE INDEX samples_geo_sample_id_index ON samples_geo USING btree(sample_id);
CREATE INDEX samples_geo_series_accession_index ON samples_geo USING btree(geo_series_accession varchar_pattern_ops);
CREATE INDEX samples_geo_accession_index ON samples_geo USING btree(geo_accession varchar_pattern_ops);
CREATE INDEX samples_geo_platform_index ON samples_geo USING btree(geo_platform varchar_pattern_ops);

-- extended design tables

DROP TABLE IF EXISTS genomes CASCADE;
CREATE TABLE genomes (id SERIAL NOT NULL PRIMARY KEY, 
name varchar(5) NOT NULL UNIQUE,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
CREATE INDEX genomes_name_index ON genomes (name);

-- ChiP-Seq tables

-- rna seq tables

DROP TABLE IF EXISTS sequence_mode CASCADE;
CREATE TABLE sequence_mode (id SERIAL NOT NULL PRIMARY KEY, 
name VARCHAR(255) NOT NULL,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
CREATE INDEX sequence_mode_index ON keywords(lower(name) varchar_pattern_ops);
INSERT INTO sequence_mode (name) VALUES ('single_end');
INSERT INTO sequence_mode (name) VALUES ('paired_end');

DROP TABLE IF EXISTS chip_seq CASCADE;
CREATE TABLE chip_seq (id SERIAL NOT NULL PRIMARY KEY, 
sample_id INTEGER NOT NULL,
seq_id varchar(255) NOT NULL,
chip_type varchar(255) NOT NULL,
cell_type varchar(255) NOT NULL,
treatment varchar(255) NOT NULL,
genome varchar(255) NOT NULL,
mode_id INTEGER NOT NULL,
read_length INTEGER NOT NULL,
reads INTEGER DEFAULT -1,
mapped_reads INTEGER DEFAULT -1,
duplicate_reads INTEGER DEFAULT -1,
pc_duplicate_reads FLOAT DEFAULT -1,
unique_reads INTEGER DEFAULT -1,
pc_unique_reads FLOAT DEFAULT -1,
peak_caller varchar(255) NOT NULL,
peak_caller_params varchar(255) DEFAULT 'n/a',
geo_series_accession varchar(255) DEFAULT 'n/a',
geo_accession varchar(255) DEFAULT 'n/a',
geo_platform varchar(255) DEFAULT 'n/a',
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE chip_seq ADD FOREIGN KEY (sample_id) REFERENCES samples(id);
ALTER TABLE chip_seq ADD FOREIGN KEY (mode_id) REFERENCES sequence_mode(id);

DROP TABLE IF EXISTS rna_seq CASCADE;
CREATE TABLE rna_seq (id SERIAL NOT NULL PRIMARY KEY, 
sample_id INTEGER NOT NULL,
gene_id INTEGER NOT NULL,
chromosome_id INTEGER NOT NULL,
start_pos INTEGER NOT NULL,
end_pos INTEGER NOT NULL,
locus varchar(255) NOT NULL,
genome_id INTEGER NOT NULL,
fpkm DOUBLE PRECISION NOT NULL,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE rna_seq ADD FOREIGN KEY (sample_id) REFERENCES samples(id);
ALTER TABLE rna_seq ADD FOREIGN KEY (gene_id) REFERENCES genes(id);
ALTER TABLE rna_seq ADD FOREIGN KEY (chromosome_id) REFERENCES chromosomes(id);
ALTER TABLE rna_seq ADD FOREIGN KEY (genome_id) REFERENCES genomes(id);

DROP TABLE IF EXISTS mutations CASCADE;
CREATE TABLE mutations (id SERIAL NOT NULL PRIMARY KEY, 
sample_id INTEGER NOT NULL,
gene_id INTEGER NOT NULL,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE mutations ADD FOREIGN KEY (sample_id) REFERENCES samples(id);
ALTER TABLE mutations ADD FOREIGN KEY (gene_id) REFERENCES genes(id);
CREATE INDEX mutations_sample_id_index ON mutations(sample_id);
CREATE INDEX mutations_gene_id_index ON mutations(gene_id);

--- Search tables ---
DROP TABLE IF EXISTS keywords CASCADE;
CREATE TABLE keywords (id SERIAL NOT NULL PRIMARY KEY, 
name VARCHAR(255) NOT NULL,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
CREATE INDEX search_keywords_name_index ON keywords(lower(name) varchar_pattern_ops);


DROP TABLE IF EXISTS genomes CASCADE;
CREATE TABLE genomes (id SERIAL NOT NULL PRIMARY KEY, 
name varchar(255) NOT NULL UNIQUE,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
CREATE INDEX genomes_name_index ON genomes(lower(name) varchar_pattern_ops);


DROP TABLE IF EXISTS sample_genome_files CASCADE;
CREATE TABLE sample_genome_files (id SERIAL NOT NULL PRIMARY KEY, 
sample_id INTEGER NOT NULL,
genome_id INTEGER NOT NULL,
vfs_id INTEGER NOT NULL,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE sample_genome_files ADD FOREIGN KEY (sample_id) REFERENCES samples(id);
ALTER TABLE sample_genome_files ADD FOREIGN KEY (genome_id) REFERENCES genomes(id);
ALTER TABLE sample_genome_files ADD FOREIGN KEY (vfs_id) REFERENCES vfs(id);
CREATE INDEX sample_genome_files_sample_id_index ON sample_genome_files (sample_id);
CREATE INDEX sample_genome_files_genome_id_index ON sample_genome_files (genome_id);
CREATE INDEX sample_genome_files_vfs_id_index ON sample_genome_files (vfs_id);


DROP TABLE IF EXISTS ucsc_track_types CASCADE;
CREATE TABLE ucsc_track_types (id SERIAL NOT NULL PRIMARY KEY, 
name varchar(255) NOT NULL UNIQUE,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
DELETE FROM ucsc_track_types;
INSERT INTO ucsc_track_types (name) VALUES ('bigWig');
INSERT INTO ucsc_track_types (name) VALUES ('bigBed');


DROP TABLE IF EXISTS ucsc_tracks CASCADE;
CREATE TABLE ucsc_tracks (id SERIAL NOT NULL PRIMARY KEY, 
sample_id INTEGER NOT NULL,
track_type_id INTEGER NOT NULL,
url varchar(255) NOT NULL,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE ucsc_tracks ADD FOREIGN KEY (sample_id) REFERENCES samples(id);
ALTER TABLE ucsc_tracks ADD FOREIGN KEY (track_type_id) REFERENCES ucsc_track_types(id);
CREATE INDEX ucsc_tracks_sample_id_index ON ucsc_tracks (sample_id);
CREATE INDEX ucsc_tracks_url_index ON ucsc_tracks (url);



DROP TABLE IF EXISTS genomic_element_types CASCADE;
CREATE TABLE genomic_element_types (id SERIAL NOT NULL PRIMARY KEY, 
name varchar(255) NOT NULL UNIQUE,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
INSERT INTO genomic_element_types (name) VALUES ('peaks');


DROP TABLE IF EXISTS genomic_elements CASCADE;
CREATE TABLE genomic_elements (id SERIAL NOT NULL PRIMARY KEY, 
sample_id INTEGER NOT NULL,
type_id INTEGER NOT NULL,
name varchar(255) NOT NULL UNIQUE,
path varchar(255) NOT NULL,
created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now());
ALTER TABLE genomic_elements ADD FOREIGN KEY (sample_id) REFERENCES samples(id);
ALTER TABLE genomic_elements ADD FOREIGN KEY (type_id) REFERENCES genomic_element_types(id);
CREATE INDEX genomic_elements_sample_id_index ON genomic_elements (sample_id);




--- Link categories to words ---


-- Some useful default entries


DELETE FROM sample_types;
INSERT INTO sample_types (name) VALUES ('Microarray');
INSERT INTO sample_types (name) VALUES ('RNA-Seq');
INSERT INTO sample_types (name) VALUES ('ChIP-Seq');

DELETE FROM section_types;
INSERT INTO section_types (name) VALUES ('Sample');
INSERT INTO section_types (name) VALUES ('Source');
INSERT INTO section_types (name) VALUES ('Extract');
INSERT INTO section_types (name) VALUES ('Labeled Extract');
INSERT INTO section_types (name) VALUES ('Hybridization');

DELETE FROM providers;
INSERT INTO providers (name) VALUES ('Affymetrix');
INSERT INTO providers (name) VALUES ('Illumina');

DELETE FROM assays;
INSERT INTO assays (name) VALUES ('Gene Expression');

DELETE FROM genomes;
INSERT INTO genomes (name, db) VALUES ('hg19', 'UCSC');
INSERT INTO genomes (name, db) VALUES ('mm10', 'UCSC');
INSERT INTO genomes (name, db) VALUES ('GRCh38', 'GENCODE');
INSERT INTO genomes (name, db) VALUES ('GRCm38', 'GENCODE');
