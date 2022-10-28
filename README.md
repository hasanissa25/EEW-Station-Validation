# Running Station Validation Script
<b>Assumptions</b>: The user has access to the AWS EC2 instance, and is logged in as the <b>ec2-user on the AWS validation instance</b>

<b>Instructions</b>:
While logged into the EC2 instance as the ec2-user and is on the AWS validation instance: 

-  `cd /home/ec2-user/EEW-Station-Validation`
-  `source venv/bin/activate`
-  `nohup stationverification {Parameters} >> logs/{name of the log file}.out &`

-  <details><summary>Parameters</summary>
      
      `N: The network code, Example: QW`

      `S: The station code, Example: QCC01`

      `L: The location code, Example: 00`

      `d: Start date, YYYY-M-D; Example: 2022-3-9`

      `e: End date, EXCLUSIVE YYYY-M-D; for a one day validation period, the end date should be startdate + 1. Example: 2022-3-15`

      `o: Output directory. Example: "/validation"`

      `s: Station xml location, if using a file instead of FDSN, Example: '/home/ec2-user/station-validation/stationverification/data/QW.xml`

      `m: Miniseed files archive location, Example: '/apollo/archive/miniseed/'`

      `l: Latency files arhcive location, Example: '/apollo/archive/latency'`

      `i: ISPAQ executable location, Example: '/home/ec2-user/ispaq/run_ispaq.py'`

      `H: State of health files arhcive location, Example: '/apollo/archive/soh/'`

      `U: Whether or not to upload results to S3 bucket, Example: True or False`

      `c: Station configuration file, if no stationXML is available, Example: /home/ec2-user/station-validation/tests/data`
</details> 


-  <details><summary>Sample calls</summary>
    <br/>
    <b>Station Verification script:</b> 

    Running the script for one day (2022-7-1): `time nohup stationverification -N QW -S QCC02 -L 00 -d 2022-7-1 -e 2022-7-2  >> logs/QCC02_log.out &`

    Running the script for 10 days (2022-7-1 To 2022-7-11): `time nohup stationverification -N QW -S QCC02 -L 00 -d 2022-7-1 -e 2022-7-11  >> logs/QCC02_log.out &`

    <b>Latency script:</b>
    
    `time nohup stationverificationlatency -N QW -S BCL01 -d 2022-6-25 -e 2022-7-5  >> logs/BCL01-Latency_log &`

    <b>Station Verification script with Station XML, and over-writing default archive directories:</b>
    
    `time nohup stationverification -N QW -S QCC01 -L 00 -d 2022-4-21 -e 2022-5-1 -m /apollo/archive/miniseed/ -l /apollo/archive/latency -i /home/ec2-user/ispaq/run_ispaq.py -H /apollo/archive/soh/ -s /home/ec2-user/station-validation/stationverification/data/QW.xml -o /validation >> logs/QCC01_log.out &`

    <b>Station Verification script with station Config file, and over-writing default archive directories:</b>
    
    `time nohup stationverification -N QW -S QCC02 -L 00 -d 2022-3-28 -e 2022-3-29 -c /home/ec2-user/station-validation/tests/data/stationQCC02.conf -m /apollo/archive/miniseed/ -l /apollo/archive/latency -i /home/ec2-user/ispaq/run_ispaq.py -H /apollo/archive/soh/ -o /validation >> logs/QCC02_log.out &`

    <b>Latency script, and over-writing default archive directories:</b>
    
    `time nohup stationverificationlatency -N QW -S BCL25 -d 2022-4-21 -e 2022-4-22 -l /apollo/archive/latency -o /validation >> logs/BCL25_log.out &</details>`






<h1>Uploading Results to GitLab (NRCan network, not on AWS)</h1>

<b>Assumptions</b>:
- The user has cloned the GitLab repository (http://gitlab.seismo.nrcan.gc.ca/eew/station-validation.git) and installed it.

- The results are on 3.96.234.48:18010, which the user can not access while being on the VPN. This can be solved by port forwarding.

- The URL provided to the upload script should be in the following template:
   - `https://3.96.234.48:18010/json/QW/{station}/{date}/`

- The current access token is valid.
   - If the access token is not valid, please go to:
   - Go to : http://gitlab.seismo.nrcan.gc.ca/eew/station-validation/-/settings/access_tokens 
   - Follow the steps on the page above, and add an access token.
   - Call the script, and include the token using -T parameter.
   - Example: uploadreport -t "QW BCH14 2022-07-16 To 2022-07-26" -w "https://3.96.234.48:18010/json/QW/BCH14/2022-07-16-2022-07-26/" -I Fortimus -T "ACCESS_TOKEN"


<b>Sample Call:</b>

    cd station-validation

    pip3 install .

    uploadreport -t "QW BCH14 2022-07-16 To 2022-07-26" -w "https://3.96.234.48:18010/json/QW/BCH14/2022-07-16-2022-07-26/" -I Fortimus

     t: Title of the wiki page
     w: The link to the webserver containing the results.
     I: The type of instrument. Nanometrics or Fortimus

# Reading Station Validation Results

<details><summary>JSON Report</summary>
<br/>
<details><summary>Metrics</summary>
Each Metric has three key value pairs

- Passed: True or False
  - Whether the list of Values has passed our validation test through the comparison of each value with the predefined thresholds

- Details: 
  
  - Empty if Passed is True, or the specific reason the validation failed if Passed is False

- Values :
  
  - The result of the metric for each day in the validation period

</details>

<details><summary>Channel Metrics</summary>

- Each Channel (HNN, HNE, HNZ) has a list of metrics that are being validated, and a Latency object

- As of June 2022, the list includes:
  - Number of gaps, Max gap, Number of overlaps, Max Overlaps, Spikes, Calibration Signal
  - Percent Below New Noise Model, Percent Above New High Noise Model, Percent availability, 
  - Latency object which contains Average latency, and Timely availability.
 
    - Average latency:
      - The average latency across the entire validation period for the specified channel
    - Timely availability:
      - The percentage of latency values that are below our threshold latency across the entire validation period for the specified channel


</details>

<details><summary>Station Metrics</summary>

- Station Metrics are metrics that are channel independent
- As of June 2022, the list includes:
  - Station latency, Clock offset, Timing quality, Clock locked, and Satellites locked


</details>
</details>

<details><summary>PDF Plot</summary>

- Probability density function plots
- As of June 2022, the X-axis is period in seconds.
  - IRIS will be adding an option to allow for Frequency on the X-axis instead

<details><summary>Passing</summary>
![image](uploads/e4e0236c77c4232ba76317441232923a/image.png)</details>
<details><summary>Failing</summary>
![image](uploads/61a5ee7b1ce9829a9ddcc81cf2d3bc7a/image.png)
![image](uploads/2642b9cda687898bbcef148a0ef55da8/image.png)</details>
</details>

<details><summary>Latency Log Plot</summary>

- The latency log plot represents all the latency values for the entire validation period

- The red vertical line represents the Data Timeliness threshold

- The data on the left of the threshold is passing data

- The data on the right of the threshold is failing data

<details><summary>Passing</summary>
![image](uploads/eeed83982d950de866c6db4285a93cfe/image.png)</details>
<details><summary>Failing</summary>
![image](uploads/3ba63fdff37b097439f4f380ca2e7584/image.png)</details>
</details>

<details><summary>Latency Line Plots</summary>

- The Latency line plots are a daily representation of the latency values, for each day in the validation period.

- The red horizontal line is the Data Timeliness Threshold

- The data above the threshold is failing data.

- The data below the threshold is passing data

<details><summary>Passing</summary>
![image](uploads/34f90711a7133fd1a5e9c3cb2cd779e6/image.png)</details>
<details><summary>Failing</summary>
![image](uploads/a3c1db285e163428c67fc587910f5ab6/image.png)</details>
</details><details><summary>Timely Availability Plot</summary>

- Timely Availability
  - Percentage of latency values that are below our predefined threshold

- Percent availability 
  - The portion of data available for each day represented as a percentage
<details><summary>Passing</summary>
![image](uploads/7e423224379ae23e6da7324b5d128d1e/image.png)</details>
<details><summary>Failing</summary>
![image](uploads/f1a4a3edc4a7878a1768c16bbb73e59d/image.png)
</details>
</details>

<details><summary>Timing Error Plot (Nanometric Stations)</summary>

- This plot is a combination of the clock offset in microseconds and the clock status

- When the clock is locked, if the clock offset value is above the positive red horizontal threshold line, or below the negative red horizontal threshold line then the data is failing.

- If the clock is unlocked, or the clock is off, further investigation is required

<details><summary>Timing Error Plot: Expected Behavior</summary>
![image](uploads/8f797b29bb3c05c95f5df7d198ab8825/image.png)</details>
<details><summary>Timing Error Plot: Requires Investigation</summary>
![image](uploads/7d34d030caf0cc22587be75349b99c6e/image.png)</details>
</details>

<details><summary>Clock Offset Plot (Fortimus Stations)</summary>

- This plot represents the clock offset in microseconds, for a single day

- If the clock offset value is above the red horizontal threshold line, then the data is failing.

<details><summary>Clock Offset Plot: Expected Behavior</summary>
![image](uploads/122d21613b8453db52f6295152222336/image.png)</details>
</details>


<details><summary>Clock Offset Log Plot (Fortimus Stations)</summary>

- This plot represents the clock offset in microseconds, for the duration of the validation period

<details><summary>Clock Offset Log Plot: Expected Behavior</summary>
![image](uploads/6f7b83c40b06f91516dfb1ad0a99a076/image.png)</details>
</details>

<details><summary>Timing Quality Plot</summary>

- Average SEED timing quality value per day

- The red horizontal line is the Timing Quality Threshold.

- Daily values above the threshold are passing

- Daily values below the threshold are failing

<details><summary>Passing</summary>
![image](uploads/5562f543745fb6eac2fe02229f00b495/image.png)</details>
<details><summary>Failing</summary>
![image](uploads/a45cae17542fc73aa9cc567812cd2eda/image.png)</details>
</details>

<details><summary>ADC Count Plot</summary>

- The value in ADC counts of the accelerometer channel for N, E and Z respectively.

<details><summary>Passing</summary>
![image](uploads/de62e2d820aa9a30e8b6cf8397d21e38/image.png)
</details>
<details><summary>Failing</summary>
![image](uploads/bfeea6d9f7b43c00728281f00877a440/image.png)
</details>
</details>

<details><summary>Max Gaps Plot</summary>

- Indicates the size of the largest gap in data encountered in each 24-hour window during the validation period

<details><summary>Passing</summary>
![image](uploads/5e414f501de1a6ca14a2caf18b90f8be/image.png)
</details>
<details><summary>Failing</summary>
![image](uploads/3d86f4645da282933ad9ad4c658ae676/image.png)
</details>
</details>

<details><summary>Number of Gaps Plot</summary>

- Indicates the number of gaps in data encountered in each 24-hour window during the validation period

<details><summary>Passing</summary>
![image](uploads/0558b1616951ff1512002648a05a646f/image.png)
</details>
<details><summary>Failing</summary>
![image](uploads/d7fc5e45a4a77e9473afaafd2d598dcb/image.png)</details>
</details>

<details><summary>Number of Overlaps Plot</summary>

- This metric reports the number of overlaps encountered in each 24-hour window during the entire validation period

<details><summary>Passing</summary>
![image](uploads/412b40561d4b4256a68fdfbcc7c61dce/image.png)
</details>
<details><summary>Failing</summary>
![image](uploads/1155644a7dc346515db1320701a0b650/image.png)
</details>
</details>

<details><summary>Spikes Plot</summary>

- This metric reports the number of times spikes were encountered in each 24-hour window during the entire validation period.

- Spikes represent that the 'Spikes detected' bit in the 'dq_flags' byte was set within a miniSEED file. 

- This data quality flag is set by some dataloggers in the fixed section of the miniSEED header when short-duration spikes have been detected in the data. 
Because spikes have shorter duration than the natural period of most seismic sensors, spikes often indicate a problem introduced at or after the datalogger

<details><summary>Passing</summary>
![image](uploads/b00900f1a66ca357ed5f3504850dc186/image.png)
</details>
<details><summary>Failing</summary>
![image](uploads/825631de9e43d31ca620b6f587519ab1/image.png)
</details>
</details>

<details><summary>Percent above New High Noise Model Plot</summary>

- Percentage of Probability Density Function values that are above the New High Noise Model. 

- This value is calculated for each 24-hour window over the entire validation period.

<details><summary>Passing</summary>
![image](uploads/6367841b061db023d1257bbe0bd2633c/image.png)
</details>
<details><summary>Failing</summary>
![image](uploads/69a64cb86adb299f34d78b8ebbb2deef/image.png)
</details>
</details>

<details><summary>Percent Below New Low Noise Model Plot</summary>

- Percentage of Probability Density Function values that are below the New Low Noise Model. 

- This value is calculated for each 24-hour window over the entire validation period.

<details><summary>Passing</summary>
![image](uploads/e1edfc4899c3c5a8fe85530f76a8d0b7/image.png)
</details>
<details><summary>Failing</summary>
![image](uploads/3991066968a193deb61f091a7f6c22b8/image.png)
</details>
</details>

# Submitting tickets and viewing results

<details><summary>Navigating to the Station-Validation GitLab project</summary>
<br/>
- Please follow this link to gain access to the project: http://gitlab.seismo.nrcan.gc.ca/eew/station-validation
<br/>

  - You will need to login to GitLab in order to gain access
  
  - If you have issues with permission, please contact me: Hasan.issa@nrcan.rncan.gc.ca 
  
  - If you successfully gained access to the link, you should find yourself at the following page:

![image](uploads/7a7f4fbf8f76f3d02d0d891f6f595900/image.png)</details>

<details><summary>Accessing Station Validation results</summary>

- You can go directly to this link: http://gitlab.seismo.nrcan.gc.ca/eew/station-validation/-/wikis/home <br/>

- Alternatively, click Wiki, from the left hand side
<br/>
![image](uploads/34a4de881f95aedbaf875f68aff2b1ab/image.png)
<br/>
- After clicking Wiki, you should find yourself at this page below: 
<br/>
![image](uploads/712d04d409b02f7fc37cd92b9ec1870d/image.png)
- From the page above, make a selection from the right hand side menu, to specify the station.

- Once inside the station wiki, you can then click any of the dropdown menus to view the results as shown below

![image](uploads/76c22ebb3d64741fb6f000aa8cc17c6b/image.png)
</details>

<details><summary>Viewing current tickets</summary>

– You can go directly to this link: http://gitlab.seismo.nrcan.gc.ca/eew/station-validation/-/issues

– Alternatively, you can follow the steps below:

– In order to view current tickets, highlight Issues on the left hand side, and click List

![image](uploads/c31b77a74a05014d74d4782c0be9328c/image.png)
– You will be redirected to the following page, with the list of the current opened tickets

![image](uploads/9f1d9fbe5d0441648aac756dd754e457/image.png)
</details>

<details><summary>Creating Tickets</summary>

- Go to: http://gitlab.seismo.nrcan.gc.ca/eew/station-validation/-/issues

- Click “New issue”, on the top right

![image](uploads/93c58d6827773faf5b81173cafcf9224/image.png)
- After clicking “New issue”, you will be redirected to the New Issue section shown below

![image](uploads/927f2981e0fd4c79d6b34ed1d3631988/image.png)
- Enter the title of the ticket, with a brief description, then click Create issue, shown above

- This will add the to the ticket to the list of issues: http://gitlab.seismo.nrcan.gc.ca/eew/station-validation/-/issues

</details>

<details><summary>Viewing Ticket board</summary>

- You can directly to : http://gitlab.seismo.nrcan.gc.ca/eew/station-validation/-/boards

- Alternatively, follow these steps:

- Highlight Issues on the left hand side, and click Boards.

![image](uploads/d5e8e5ea58b18eb22ef649807fb39ab9/image.png)
- You should be able to see the Issue Boards with the open tickets, the ones in Development, and the ones that have already been closed.

![image](uploads/851fc360b772f82cf05bd1e7aae922a4/image.png)
</details>
