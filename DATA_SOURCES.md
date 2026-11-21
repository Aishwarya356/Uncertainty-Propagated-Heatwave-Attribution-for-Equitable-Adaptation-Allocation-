# Candidate Data Sources for Vulnerability and Equity

## Study places

These are the 10 locality/district labels in the existing `localities.csv` inside the heatwave-results ZIP. The district names below are copied from that file; they are not a claim that locality boundaries have been verified against census boundaries.

| Locality | District in existing results | Heatwave events |
|---|---|---:|
| Chennai | Chennai | 18 |
| Mahabalipuram | Chengalpattu | 13 |
| Marakkanam | Villupuram | 12 |
| Cuddalore | Cuddalore | 9 |
| Nagapattinam | Nagapattinam | 8 |
| Adirampattinam | Thanjavur | 8 |
| Mimisal | Pudukkottai | 8 |
| Ramanathapuram | Ramanathapuram | 1 |
| Thoothukudi | Thoothukkudi | 1 |
| Kanyakumari | Kanniyakumari | 0 |

The last two district labels have spelling variants between files/portals. Keep the original locality table as the join reference and record any normalized name alongside the source data. Kanyakumari remains in the vulnerability template even though the heatwave event catalog has no event for it.

## Recommended official sources

The proposal in `FDS_Review1_Final.docx` names Census of India 2011, SECC 2011, district health-infrastructure records, and PHC/hospital-bed density as possible inputs. The sources below are suitable starting points, not evidence that the values have already been collected. Several provide district, town, ward, or village data rather than data for a heatwave locality as defined in the event archive.

### 1. Population age shares and base population

**Census of India 2011 Primary Census Abstract (PCA)** — [Population Finder](https://censusindia.gov.in/census.website/en/data/population-finder), [Census tables](https://censusindia.gov.in/census.website/data/census-tables), and the official Tamil Nadu PCA catalog, for example [Chennai town/village/ward PCA](https://censusindia.gov.in/nada/index.php/catalog/6794).

- **Indicators to collect:** population total as denominator; population ages 0–6 (published as a PCA age group); SC/ST counts if relevant to the approved equity definition; household counts.
- **Geographic coverage:** Census tables can reach district, sub-district, town, village, and ward depending on table. The PCA town/village/ward catalog describes those geographic levels. Match each project locality to its actual town, village, ward, or component geographies before using it.
- **Access limitations:** 2011 is old and administrative boundaries have changed. “Child share” must be defined: the PCA's 0–6 group is a practical young-child indicator, not all children under 18. The locality names in the heatwave data may refer to a settlement or point rather than a census unit. Do not copy district totals and label them locality values.
- **Use in template:** child population share can be calculated as PCA population ages 0–6 divided by the matching area's total population, if that definition is accepted. This is not yet filled in.

**Census of India 2011 Table C-14, five-year age groups** — [Tamil Nadu C-14 table and description](https://censusindia.gov.in/nada/index.php/catalog/1572/study-description), plus [C-14 City table](https://censusindia.gov.in/nada/index.php/catalog/1640).

- **Indicators to collect:** counts for ages 60–64, 65–69, 70–74, 75–79, and 80+; total population; optionally age not stated. Add the 60+ groups for an elderly-population numerator and divide by the matching total.
- **Geographic coverage:** the Tamil Nadu table describes age distributions by district, rural/urban residence, and sex; a separate city table is available. Coverage is not uniformly at each small settlement or ward.
- **Access limitations:** the data are from 2011. The precise 60+ share cannot be taken from the heatwave CSV. If only district values are available, label them as district proxies and do not present them as locality observations. A city may have a separate table; verify the exact city unit.
- **Use in template:** keep the value blank unless the age count and total population use the same geography and year. The proposal does not set the elderly age threshold; 60+ is a candidate definition to confirm.

### 2. Housing quality and household amenities

**Census Houselisting and Housing Census 2011 tables** — [HL-01: condition of occupied census houses](https://censusindia.gov.in/nada/index.php/catalog/7782/study-description), [HL-02A: roof material](https://censusindia.gov.in/nada/index.php/catalog/7881), [HL-04: household size and dwelling rooms](https://censusindia.gov.in/nada/index.php/catalog/8277), [HL-11: drinking water, electricity, and latrine](https://censusindia.gov.in/nada/index.php/catalog/8970), and [HL-14: amenities and assets, Chennai example](https://censusindia.gov.in/nada/index.php/catalog/9901). Use the catalog to locate the matching Tamil Nadu district/town tables.

- **Indicators to collect:** share of households in dilapidated houses; non-permanent roof/wall/floor material; no electricity; no latrine; unsafe or distant drinking-water source; overcrowding (for example, more than one person per room, if the source supports that calculation). Select indicators before combining them.
- **Geographic coverage:** Census housing tables and District Census Handbooks may provide town/village/ward or district data, depending on the specific table. The [District Census Handbook catalog](https://censusindia.gov.in/nada/index.php/catalog/45344) describes PCA household amenities and village/town directory material for Chennai; analogous handbooks are listed by district in the Census catalog.
- **Access limitations:** these are 2011 conditions and may be badly out of date for current adaptation planning. Some tables are available only for specific administrative units. “Housing vulnerability” is not a single source column: define a transparent measure (or keep the component percentages separately) and record its denominator and year.

### 3. Poverty or deprivation

**Socio-Economic and Caste Census (SECC) 2011** — [Tamil Nadu Rural Development & Panchayat Raj description](https://www.tnrd.tn.gov.in/schemes/cen_secc_13.html).

- **Indicators to request or check availability of:** household deprivation criteria/priority categories, housing condition, landlessness, occupation, education, disability, and asset-related deprivation. Use only fields whose release and privacy conditions allow analysis.
- **Geographic coverage:** SECC was carried out in rural and urban areas. The Tamil Nadu department describes household and individual information and verification processes. Publicly usable tables may not include all household-level fields or a stable crosswalk to the project localities.
- **Access limitations:** household/microdata access is restricted or sensitive; caste/religion person-level information is explicitly not public on the cited state page. It is a 2011 survey. Do not seek or publish identifiable household data. If local aggregation cannot be lawfully accessed, leave the template blank and use a clearly labeled public aggregate alternative.

**NITI Aayog National Multidimensional Poverty Index (MPI)** — [district-wise NFHS-5 MPI page](https://www.niti.gov.in/hi/node/868).

- **Indicators to collect:** district MPI score or headcount and the published deprivation dimensions/indicators, such as health, education, and living standards.
- **Geographic coverage:** district-level, using NFHS-5 (2019–21) data; not settlement-level.
- **Access limitations:** a district score is a contextual proxy for every locality in that district, not a measured locality deprivation rate. It is a composite index, so document its year and avoid treating it as directly comparable to a household-level rate.

### 4. Healthcare access and adaptive capacity

**Tamil Nadu Department of Economics and Statistics (DES), Statistical Handbooks** — [latest handbook/publication listing](https://www.des.tn.gov.in/en/node/346), [District Handbook description](https://www.des.tn.gov.in/en/node/32), and an example chapter [Medical and Health](https://des.tn.gov.in/sites/default/files/2025-07/14.%20MEDICAL%20AND%20HEALTH.pdf).

- **Indicators to collect:** PHCs, urban PHCs, CHCs, hospitals, beds, doctors/nurses where available; ideally facility coordinates and operating status. Calculate facilities or staffed beds per population only after matching geography and year.
- **Geographic coverage:** handbook tables include state and district figures; the DES describes District Handbooks as including district and sometimes taluk/block detail. Some municipal handbooks may have corporation/municipality coverage.
- **Access limitations:** older editions and changing administrative boundaries can limit comparability. A facility count does not show travel time, opening hours, staffing, or heat-treatment capacity. Confirm table year and denominator.

**Tamil Nadu Health Management Information System (TN-HMIS)** — [official login portal](https://tnhmis.tn.gov.in/AHIMSG5/hissso/Login) and [about the system](https://www.tnhmis.tn.gov.in/AHIMSG5/hissso/jsp/about.html).

- **Indicators to collect/request:** facility-level PHC/CHC/hospital registry; beds; staff; services; utilization and reporting indicators; facility location for distance-to-care analysis.
- **Geographic coverage:** the portal describes facility performance at block, district, and state levels and networks primary through tertiary facilities.
- **Access limitations:** it is a login portal. Detailed facility data may require an account or department permission. Use public exports or request an aggregate dataset; do not treat access as guaranteed. Reporting coverage and facility completeness should be checked.

**National Health Mission Rural Health Statistics / Health Dynamics of India** — [NHM Rural Health Statistics resources](https://nhm.gov.in/index1.php?lang=1&level=0&lid=43&linkid=39).

- **Indicators to collect:** rural sub-centres, PHCs, CHCs, required vs. available facilities, beds, and workforce gaps.
- **Geographic coverage:** primarily rural health-system summaries, commonly state/district; use the edition's own tables to confirm granularity.
- **Access limitations:** may exclude or separately classify urban services and does not necessarily give exact facility coordinates or locality catchments. Availability and reporting year vary by edition.

**NFHS-5/6 fact sheets and district estimates** — [NFHS-5 district fact-sheet catalog on data.gov.in](https://www.data.gov.in/catalog/national-family-health-survey-5-nfhs-5-india-districts-factsheet-data-provisional), [NFHS-5 Tamil Nadu state fact sheet](https://www.mohfw.gov.in/sites/default/files/NFHS-5_Phase-II_0.pdf), and [NFHS-6 fact-sheet compendium](https://nhm.gov.in/New-Update-2025-26/NFHS-6-factsheet.pdf).

- **Indicators to collect:** household wealth/deprivation context, sanitation, drinking water, health insurance, use of public health services, maternal/child health and nutrition indicators where relevant. Select indicators tied to the project's definition of adaptive capacity.
- **Geographic coverage:** state and district estimates; district fact sheets may reflect the boundary definitions used when the survey was designed. Not locality- or ward-level.
- **Access limitations:** survey estimates have sampling uncertainty and are not exact counts for small localities. NFHS-5 (2019–21) and NFHS-6 (2023–24) use different years; do not combine silently. Check the fact-sheet notes, district boundary, and indicator denominator before use.

## Geographic and date matching rules

1. First identify what each locality name means in the heatwave results: municipality/town, village, ward, or a point representing a wider area. The archived names and coordinates alone do not establish census boundaries.
2. Prefer the same geography for all indicators. If a district proxy is unavoidable, record it as a district proxy and use the same proxy logic for every locality.
3. Census 2011 and newer health/NFHS records may use different district boundaries. For example, Chengalpattu was carved from the former Kancheepuram district in 2019, according to the [Chengalpattu district administration](https://chengalpattu.nic.in/about-district/). Crosswalk before comparing.
4. Record each value's source, publication/survey year, geographic unit, numerator, denominator, and any transformation. Keep the raw source values separately so the summary can be checked.

## Suggested meanings for the template fields

- **Elderly population share:** candidate definition is residents aged 60+ divided by total residents in the same area and year. Confirm the cutoff with the project supervisor.
- **Child population share:** use the official 0–6 Census group only if the project accepts “young-child share.” If “children” means under 18, use age bands supporting that threshold or leave blank; do not relabel 0–6 as all children.
- **Housing vulnerability:** do not enter a subjective single score. First choose and document one measurable rate or a documented index. Keep source components and formula in notes/supporting data.
- **Deprivation indicator:** prefer a published deprivation rate/index with known geography, year, and definition. A district index remains a district proxy.
- **Healthcare access:** prefer a measurable rate such as staffed public beds or PHCs per population, or a facility travel-time measure. State which one is used; a facility count alone is not access.

No values have been downloaded or entered in `vulnerability_dataset.csv`.
