# Age data collection status

## What I found

The Census of India 2011 C-14 table contains population counts by five-year age groups and residence/sex. Its Tamil Nadu catalog entry is [C-14: Population in five year age group by residence and sex, Tamil Nadu - 2011](https://censusindia.gov.in/nada/index.php/catalog/1572). The official table file has been downloaded to `official_source_files/DDW-3300C-14.xls` (Excel 97–2003 format).

The current file is the state C-14 table, not an already matched table for all ten project localities. The source descriptions identify district/residence/sex coverage; the downloadable file still needs to be inspected to confirm its exact rows and geography before any values can be calculated. The Census also lists a separate [C-14 city table](https://censusindia.gov.in/nada/index.php/catalog/1640), but that does not establish matching coverage for every settlement in this project.

The existing project names and districts are in `vulnerability_dataset.csv`. These names have not been demonstrated to match Census towns, wards, or villages. For example, a project locality label may refer to a point or broader area. Therefore no Census district or city figure has been copied into a locality row.

## Measures to calculate after geographic matching

- **Elderly share (candidate definition):** (population aged 60–64 + 65–69 + 70–74 + 75–79 + 80+) divided by total population, for the same Census geography, year, residence category, and sex coverage. Record age-not-stated handling and confirm that 60+ is the project’s agreed definition.
- **Young-child share:** Census PCA population aged 0–6 divided by total population in the same matched geography. The PCA is not a measure of all children under 18. See the official [Chennai PCA catalog example](https://censusindia.gov.in/nada/index.php/catalog/6794); use the corresponding Tamil Nadu Census unit for each locality after matching.

## What remains before entering values

1. Open `official_source_files/DDW-3300C-14.xls` in Excel or LibreOffice and use **Save As** to save a copy as `official_source_files/DDW-3300C-14.xlsx`. Keep the downloaded `.xls` unchanged. Alternatively, share the source workbook with all sheets intact in `.xlsx` format.
2. Identify each project locality’s Census 2011 geography (town, village, ward, or a documented set of component units). Use the corresponding PCA unit(s) for the 0–6 count and total population. A district-only match is not a locality match.
3. Reconcile boundary and naming differences between the project locality/district list and Census 2011 geography. If the boundary cannot be matched, leave that locality blank or document a separately labeled district proxy; do not place a proxy in a locality-level field.
4. Once the workbook can be read and the geography is confirmed, calculate shares from the raw numerator and denominator and document the source URL, 2011 year, geography, and formula for every value.

## Current status

No age values have been added to `vulnerability_dataset.csv`. No values have been inferred or invented. Housing collection has not started because the requested workflow is to finish one dataset at a time and the age dataset still needs conversion/inspection and locality matching. No model has been trained.

## Follow-up: workbook coverage and place matching

The official catalog for the downloaded workbook describes it as a 2011 table with age groups, area name, and residence/sex dimensions. The catalog says the table is geographically organized at **state and district** levels; this is the catalog entry for the exact downloaded file: [DDW-3300C-14.xls, Census C-14 Tamil Nadu](https://censusindia.gov.in/nada/index.php/catalog/1572). The physical workbook could not be opened in this environment: the installed Python reader set has no legacy `.xls` reader, and Windows denied programmatic Excel automation. Therefore its worksheet names, actual row count, and exact column layout have not been independently inspected here. The catalog metadata, rather than a direct workbook inspection, is the source for the structure stated above.

The locality matching work is recorded in `CENSUS_LOCALITY_MAPPING.csv`. The Census provides official town/village/ward PCA tables with population totals and 0–6 population, including the study places or their close name variants. A PCA town/village/ward catalog is not itself proof that a heatwave-study point represents the whole listed unit; the mapping therefore identifies candidates and gives a confidence note instead of silently resolving boundaries.

The downloaded C-14 Tamil Nadu workbook does **not** provide 60+ age groups for the candidate towns or villages: its catalog coverage is state/district. The Census publishes a separate [C-14 City table](https://censusindia.gov.in/nada/index.php/catalog/1640) for city units; its actual downloaded contents must be checked to see which study cities it includes. Town-level or village-level age groups are not established by the C-14 file already downloaded.

For a matched unit with age data, calculate:

`elderly population share = (60–64 + 65–69 + 70–74 + 75–79 + 80+) / All ages`

Use the same unit, year (2011), residence category, and sex coverage in every term. Use total males plus females, or one sex consistently. Do not add “age not stated” to the numerator; use the source's all-ages total as denominator and document this choice. This share should remain blank until the exact unit has an age-group numerator and matching all-ages denominator.

Before any locality value is entered, confirm the point-to-boundary assignment for every row in `CENSUS_LOCALITY_MAPPING.csv`. In particular, Adirampattinam has both a similarly named village and a town; Mimisal is listed by Census as “Mimisal Chatrapattinam”; and Kanyakumari is a spelling variation from Kanniyakumari and also has a same-name village. Mahabalipuram is listed as Mamallapuram under the 2011 Kancheepuram district, before Chengalpattu became a separate district.

## C-14 City workbook checked

The official [C-14 City catalog page](https://censusindia.gov.in/nada/index.php/catalog/1640) provides the workbook `DDWCT-0000C-14.xls`, which was downloaded to `official_source_files/DDWCT-0000C-14.xls`. This is a distinct Census product from the Tamil Nadu C-14 district workbook downloaded earlier.

I inspected the workbook with an `.xls` reader. It has one worksheet (`Sheet1`), six header rows, and 9,595 data rows for 505 city codes across India. Each city has 19 age-group rows: All ages, 0–4 through 80+, and Age not stated. The data columns identify the state code, town code, area name, age group, and total/rural/urban population counts split by persons, males, and females. There are 32 Tamil Nadu city codes in this file. The source is 2011 Census data at city level.

Of the ten candidate units in `CENSUS_LOCALITY_MAPPING.csv`, four town/city codes are present with the needed age bands and an All ages total: Chennai (803339), Cuddalore (803650), Nagapattinam (803674), and Thoothukkudi (803821). Their 60+ person counts and shares, calculated from the Total Persons column, are recorded in `AGE_DATA_RESULTS.csv`. For each, 60+ count is the sum of the 60–64, 65–69, 70–74, 75–79, and 80+ rows; the share is that sum divided by the same city’s All ages Total Persons count. Age not stated is excluded from the numerator. The five age rows plus Age not stated sum to the All ages count for each of the four cities.

The remaining six candidate codes are not present in the C-14 City workbook: Mamallapuram, Marakkanam, both Adirampattinam candidates, Mimisal Chatrapattinam, Ramanathapuram, and Kanniyakumari. The results CSV leaves their counts and shares blank. The workbook’s city-level count is a verified measurement for the Census city code, but the project-to-Census boundary match is still marked Medium or Low in the mapping. Therefore the separate `verified study-locality 60+ share` column remains blank for all ten until the point-to-boundary matches are confirmed. No district values are used as substitutes.

The underlying Census-unit ratios are useful checks, but they are not yet approved as values for the study localities. Do not copy them into `vulnerability_dataset.csv` until the match is confirmed.
