# Healthcare access data notes

## What I checked

I checked the project's healthcare source suggestions and the study-locality/district labels in `DATA_SOURCES.md`, then reviewed official Tamil Nadu and Government of India sources. The study localities and their district labels below are the labels in the heatwave results; they do not independently prove a town boundary.

## Usable official district context

The Tamil Nadu Health and Family Welfare Department's [Policy Note 2024–25](https://portal.tndphpm.com/tndphpmfiles/1719998290_hfw_policy_note_english.pdf) has a table titled “No. of Health Institutions” with district totals for Health Sub-Centres (HSCs), Primary Health Centres (PHCs), Government Hospitals, Medical & Dental College Hospitals, and Indian Medicine Hospitals & Dispensaries. I transcribed the entries for the ten districts corresponding to the project's study-locality labels into `HEALTHCARE_DATA_RESULTS.csv`.

- **Geographic level:** district. Every populated count in the results file is explicitly a district count; no locality-level facility counts were found for this pass.
- **Year:** the document is the 2024–25 policy note. The table itself does not state an “as of” date or clearly specify the reference year for the facility totals. The results therefore label the reference as “2024–25 policy note; table reference date not stated,” rather than claiming the totals are measured in 2024–25.
- **Meaning:** each number is a count of institutions in that facility category in the district. It is not a measure of travel time, operating status, staffing, bed availability, heat-treatment capacity, or the share of residents with access.
- **Missing/dash values:** a dash printed in the table is recorded as a dash and the numeric count is left blank. A dash is not assumed to mean zero.
- **District matching:** the `study_locality` and `study_district_label` fields are only cross-references to the project's heatwave labels. The facility count's actual unit is the district name printed in the policy note. District names are modern policy-note labels; they may not match 2011 Census boundaries. In particular, Mahabalipuram's Census candidate is in former Kancheepuram while the heatwave file associates it with present-day Chengalpattu. Verify the study point's boundary before making cross-year comparisons. Spelling variants include Thoothukkudi/Thoothukudi and Kanniyakumari/Kanyakumari.

Facility categories are not interchangeable. HSC is a sub-centre; PHC is a primary health centre; “Government Hospital” is the table's own broad category; Medical & Dental College Hospitals are reported separately; and Indian Medicine Hospitals & Dispensaries are not the same as allopathic hospitals. The table does not separately identify CHCs or UPHCs, and its PHC total should not be re-labelled as an UPHC count.

## Other official sources reviewed

### Health Dynamics of India 2022–23

The Ministry of Health and Family Welfare [Health Dynamics of India (Infrastructure & Human Resources) 2022–23 report](https://www.mohfw.gov.in/sites/default/files/Health%20Dynamics%20of%20India%20%28Infrastructure%20%26%20Human%20Resources%29%202022-23_RE%20%281%29.pdf) is an official national report. Its published summary tables include state totals; for example, the hospital table is explicitly “as on 31 March 2023.” These state-level values cannot distinguish the ten localities or their districts, so they are not copied into the results file. Use the report's own table notes for any future indicator; different tables can have different reference dates.

### Tamil Nadu Health Facilities 2023 table

The [official Health Facilities, Tamil Nadu–2023 PDF](https://rabiesfreeindia.mohfw.gov.in/resources/uploads/PageContentPdf/174419151310.pdf) lists health-unit district (HUD) and district rows, including rural PHC categories, rural health sub-centres, urban PHCs, and other institutions. Its `Block` field is a number of blocks, not a facility count or a named locality crosswalk. The table's geography is not the study town, so I did not use its figures as locality counts or combine it with the policy-note categories. The PDF text could be checked online, but a local copy could not be obtained/inspected in this pass.

### Official directory of named health centres (2016)

The Government of India's [All India Health Centres Directory resource](https://www.data.gov.in/resource/all-india-health-centres-directory-7th-october-2016) is a potential route to named PHCs, sub-centres, CHCs and hospitals. Its resource is dated 7 October 2016 and includes state, district, subdistrict, facility type and facility name fields. The site displays only a preview unless the download form is completed; download requires choosing a purpose and solving a CAPTCHA. I did not attempt to bypass the CAPTCHA, and the full file was not downloaded. Even if obtained, it is old and would need checks for duplicates, facility status, boundary names and missing geographies before it could support subdistrict counts.

### Tamil Nadu HMIS and district handbooks

The [Tamil Nadu HMIS portal](https://www.tnhmis.tn.gov.in/AHIMSG5/hissso/Login) and its [about page](https://www.tnhmis.tn.gov.in/AHIMSG5/hissso/jsp/about.html) describe block/district/state monitoring, but detailed facility records are behind a login. The Department of Economics and Statistics says its [district handbooks](https://www.des.tn.gov.in/en/node/32) may contain district, taluk and block details; its [Medical and Health chapter](https://des.tn.gov.in/sites/default/files/2025-07/14.%20MEDICAL%20AND%20HEALTH.pdf) gives broader official statistics. These sources may be useful for a manually resolved subdistrict or town, but the editions and tables need to be checked for the same unit, year and definition before use. District-level beds/doctors or totals are not locality-level access.

## Interpretation and limits

The district counts are useful background context only. They are not ten locality observations and should not be copied into `vulnerability_dataset.csv`'s healthcare-access field as if they were town counts. A district with many facilities may also have a large population or facilities far from the study settlement. A count alone cannot show whether a facility is open, staffed, equipped for heat illness, or reachable during an extreme heat event.

The project still needs a consistent healthcare-access measure. A practical next measure could be (a) travel time/distance from each verified locality boundary to operating public facilities, or (b) facilities or staffed beds per population at a matched, documented geography. The project must choose which, and use comparable dates and facility definitions for every locality.

## Manual download instructions for the 2016 named-facility directory

1. Open the [official resource page](https://www.data.gov.in/resource/all-india-health-centres-directory-7th-october-2016).
2. Use the CSV download button. Select **Non Commercial** and **Academia** if asked for a purpose.
3. Complete the CAPTCHA yourself and submit the download form.
4. Save the downloaded CSV in the project's `official_source_files` folder and send/leave that file in this project folder.
5. Before it is used, confirm its fields and row count, filter Tamil Nadu, inspect facility types and subdistricts, and resolve whether each study locality is a town, village or broader point. Do not treat a same-named facility or district total as a locality count.

## What remains missing

- Facility-level records with names and locations for a recent, common reference date.
- Verified locality boundaries for all ten study places. Adirampattinam has both a town and a similarly named village candidate; Mimisal's compound Census village match is uncertain.
- A documented measure of access (distance/travel time, or a properly matched facility/bed rate), not just district facility totals.
- For facility counts, a rule for which providers count (public only or public and private; PHC/UPHC/CHC/hospital; operating status) and a consistent denominator/year.
- A decision about whether district context is useful as a separate column in the final analysis. It must remain labelled as district context if used.

No changes were made to `vulnerability_dataset.csv`, and no vulnerability score was calculated.
