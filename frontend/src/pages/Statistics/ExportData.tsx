import { Button, Checkbox, Flex, Grid, Modal } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import React, { useState } from 'react';

// Interfaces

// Interface for the scores object in the PolicyObject interface
interface Policy {
  [key: string]: number;
}

// Interface for each policy object in the appData array
interface PolicyObject {
  id: string;
  name: string;
  logo_url: string;
  policy: string;
  scores: Policy;
  status: string;
}

// Interface for the props passed to the ExportData component
interface ExportDataProps {
  appData: PolicyObject[];
}

// ExportData component

export default function ExportData({ appData }: ExportDataProps) {

  // open and close the modal
  const [opened, { open, close }] = useDisclosure(false);

  // State and state update function for selected headers
  const [selectedHeaders, setSelectedHeaders] = useState<string[]>([
    'id',
    'name',
    'logo_url',
    ...Object.keys(appData[0].scores),
    'status',
    'policy'
  ]);

  // Function to handle toggling of headers
  function handleHeaderToggle(header: string) {
    setSelectedHeaders((prevSelectedHeaders) => {
      if (prevSelectedHeaders.includes(header)) {
        // If the header is already selected, remove it from the selectedHeaders array
        return prevSelectedHeaders.filter(
          (selectedHeader) => selectedHeader !== header
        );
      } else {
        // If the header is not selected, add it to the selectedHeaders array
        return [...prevSelectedHeaders, header];
      }
    });
  }

  // Function to download CSV file
  function downloadCSV() {
    // Convert the appData array to CSV format
    const csvData = convertToCSV(appData);
    // Create a Blob object from the CSV data
    const blob = new Blob([csvData], { type: 'text/csv;charset=utf-8;' });
    // Create a download link element
    const link = document.createElement('a');
    // Set the link's href to the URL of the Blob object
    link.setAttribute('href', URL.createObjectURL(blob));
    // Set the link's download attribute to specify the file name
    link.setAttribute('download', 'appData.csv');
    // Set the link's visibility to hidden
    link.style.visibility = 'hidden';
    // Append the link to the document body
    document.body.appendChild(link);
    // Programmatically click the link to trigger the download
    link.click();
    // Remove the link element from the document body
    document.body.removeChild(link);
  }

  // Function to convert data to CSV format
  function convertToCSV(data: PolicyObject[]): string {
    const csvRows = [];

    const headers = [
      'id',
      'name',
      'logo_url',
      ...Object.keys(data[0].scores),
      'status',
      'policy'
    ];

    // Add headers row to the CSV rows array
    csvRows.push(selectedHeaders.join(';'));

    // Add data rows to the CSV rows array
    for (const row of data) {
      const values = [
        row.id,
        row.name,
        row.logo_url,
        ...Object.values(row.scores),
        row.status,
        row.policy.replace(/\n|\r/g, '').replaceAll(';', '|'),
      ].map((value) => String(value)); // Convert each value to a string

      // Filter values based on the selected headers
      const filteredValues = values.filter(
        (_, index) => selectedHeaders.includes(headers[index])
      );

      // Join the filtered values with a ';' delimiter and add to the CSV rows array
      csvRows.push(filteredValues.join(';'));
    }

    // Join the CSV rows with a newline character and return the final CSV data
    return csvRows.join('\n');
  }

  // Render component
  return (
    <>
      <Grid>
        <Grid.Col span={9}></Grid.Col>
        <Grid.Col span={3} sx={{ justifyContent: 'end', display: 'flex' }}>
          {/* Button to open the modal for selecting headers */}
          <Button color="dark" onClick={() => open()}>
            Export data
          </Button>
        </Grid.Col>
      </Grid>

      <Modal
        opened={opened}
        onClose={close}
        title="Select Headers"
      >
        <Flex
          gap="md"
          justify="flex-start"
          align="flex-start"
          direction="column"
          wrap="wrap"
        >
          {/* Render checkboxes for each header */}
          {['id', 'name', 'logo_url', ...Object.keys(appData[0].scores), 'status', 'policy'].map((header) => (
            <Checkbox
              key={header}
              label={header}
              checked={selectedHeaders.includes(header)}
              onChange={() => handleHeaderToggle(header)}
            />
          ))}
        </Flex>
        {/* Button to initiate the download of the CSV file */}
        <Button color="teal" mt="md" onClick={() => downloadCSV()}>
          Export
        </Button>
      </Modal>
    </>
  );
}
