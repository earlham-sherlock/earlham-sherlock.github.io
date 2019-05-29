
Sherlock is an open source data platform, developed in the [Korcsmaros Group](http://www.earlham.ac.uk/korcsmaros-group) (Earlham Institute, Norwich, UK) to store, analyze and integrate bioinformatics data.


### Features
* **store** all datasets in a redundant, organized cloud storage
* **convert** all datasets to common, optimized file formats
* **execute** analytical queries on top of data files
* **share** datasets among different teams / projects
* **generate** operational datasets for certain services or collaborators


### High-level overview and presentations
* [Blog post, introducing Sherlock](http://www.earlham.ac.uk/articles/sherlock-elementary-genomics)
* [Intro presentation](https://docs.google.com/presentation/d/1DjXmMk_MBsZ375u7tQHWIV9Wsnyx-yl2XcmlYWfaFv0/edit?usp=sharing)


### More technical documentation and examples
* [Under the hood: basic components](basic_components.md)
* [Deployment guide](deployment_guide.md)
* [Backup and restore the metadata](backup_restore.md)
* Loading bioinformatics data into the Data lake
  * [Data lake](data_lake.md) structure and schema initialization
  * Loading [interaction data](loaders/load_interaction_data.md)
  * Loading [localization data](loaders/load_localization_data.md)
  * Loading [genomic sequence data](loaders/load_sequence_data.md)
  * Loading [gene annotation data](loaders/load_gene_annotation_data.md)
  * Loading [molecule ID mapping data](loaders/load_mapping_data.md)
* Example queries
  * [Query Intact protein interactions and mapping them to Uniprot IDs](example_queries/simple_mapping.md)
  * [Select proteins from a given human tissue](example_queries/filter_proteins_from_tissue.md)
  * [Filtering human Intact interactions based on tissue](example_queries/filter_interactions_from_tissue.md)
  * [Enrich protein list with internal interactions (and potentially with first neighbours)](example_queries/enrich_protein_list.md)
  * [Build brain-specific molecular network, based on Bgee and IntAct](example_queries/brain_specific_network.md)
  * [Fetching a sequence region around an point mutation](example_queries/sequence_region.md)
  

### Your feedback
... is very important for us, feel free to send it to [us](http://www.earlham.ac.uk/korcsmaros-group)! :)

---
© 2018, 2019 Earlham Institute ([License](./sherlock_license.md))