# Test environment for cyclical pointing tasks

This is a simple test environment for logging cyclical pointing task trials, as described in the ISO 9241-9 standard. The provided configuration file sets up a reciprocal (cyclical) task with nine targets. Mouse movement and clicks as well as information about the used (randomized) test setup are logged in a timestamped, uniquely named log file.

All targets in the trial are drawn on screen at the beginning of the trial, no target highlighting is implemented.

(Written for a research project at Helsinki Institute for Information Technology.)

## Requirements
- Python 2.7
- installed libraries: Tkinter, pygame
- should work on Linux, Windows and OS X (Ubuntu and Windows 7 tested)

## Test setups

Test setups are pre-defined in `config`. The comment lines in the `config` file assist in editing test setups if required. The test environment passes through all D, W combinations in a randomized order. After all combinations have been used, the test setups are randomized again.

A trial with nine targets always ends after 27 left mouseclicks (three rounds are done). Logging only starts after the first mouseclick is registered.

### Index of difficulty values covered by the default test setups

<table>
    <thead>
        <tr>
            <th>D / W</th>
            <th>100</th>
            <th>80</th>
            <th>60</th>
            <th>40</th>
            <th>20</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th>700</th>
            <td>3.0</td>
            <td>3.3</td>
            <td>3.6</td>
            <td>4.2</td>
            <td>5.2</td>
        </tr>
        <tr>
            <th>600</th>
            <td>2.8</td>
            <td>3.1</td>
            <td>3.4</td>
            <td>4.0</td>
            <td>4.9</td>
        </tr>
        <tr>
            <th>500</th>
            <td>2.6</td>
            <td>2.8</td>
            <td>3.2</td>
            <td>3.7</td>
            <td>4.7</td>
        </tr>
        <tr>
            <th>400</th>
            <td>2.3</td>
            <td>2.6</td>
            <td>2.9</td>
            <td>3.4</td>
            <td>4.4</td>
        </tr>
        <tr>
            <th>300</th>
            <td>2.0</td>
            <td>2.2</td>
            <td>2.5</td>
            <td>3.0</td>
            <td>4.0</td>
        </tr>
    </tbody>
</table>

(D values approximate.)

## Log files

Log files will be written into a subdirectory named `logs`. Test setup data and the name of the test subject (filled in at the startup prompt) are logged at the beginning of the file. The rest of the lines consist of a timestamp (in seconds after the start of logging) and x and y coordinates of the mouse cursor. Mouseclick lines are otherwise identical but have a `CLICK` identifier at the end of the line.

### Example log file

    # Subject name: Test Subject
    # Target width: 80
    # Target distance: 591

    0.0000	634	99
    0.0102	634	99
    0.0203	634	99
    0.0305	634	100
    0.0406	634	100
    0.0508	634	100
    0.0610	634	101
    0.0711	634	102
    0.0813	634	104
    0.0915	634	106
    0.0916	634	106	CLICK
    0.1016	635	109
    0.1118	635	109
    ...

### A note on operating systems

On OS X and Linux systems filenames are timestamps in the following format:

`yyyy-mm-dd-hh:mm:ss.microsec.log`

On Windows systems, colon symbols (`:`) are replaced with full stops (`.`):

`yyyy-mm-dd-hh.mm.ss.microsec.log`

On Windows, log files also use CR + LF newlines instead of the simple LF newlines used on Unix based systems.
