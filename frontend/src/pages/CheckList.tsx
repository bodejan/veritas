import { Button, FileInput, Stack, Text, Textarea, Title, LoadingOverlay, Box } from '@mantine/core';
import { useForm } from '@mantine/form';
import React, { Dispatch, ReactElement, SetStateAction, useState } from 'react';
import { useDisclosure } from '@mantine/hooks';
import { useNavigate } from "react-router-dom";

type FormData = {
  category: string;
  numApps: number;
};

interface Policy {
  [key: string]: number;
}

interface PolicyObject {
  id: string;
  name: string;
  image: string;
  policies: Policy;
}

interface CheckListProps{
  setAppData: Dispatch<SetStateAction<PolicyObject[]>>,
}

export default function CheckList({setAppData}: CheckListProps): ReactElement<CheckListProps> {
  const navigate = useNavigate();

  const [visible, { toggle }] = useDisclosure(false);
  
  const form = useForm<FormData>({
    initialValues: {
      category: '',
      numApps: 1,
    }
  });

  const { errors, getInputProps } = form;
  const [appList, setAppList] = useState<string[]>([]);

  const mockdata: PolicyObject[] = JSON.parse(JSON.stringify([
    {
      "id": "com.google.android.youtube",
      "name": "YouTube",
      "image": "https://play-lh.googleusercontent.com/lMoItBgdPPVDJsNOVtP26EKHePkwBg-PkuY9NOrc-fumRtTFP4XhpUNk_22syN4Datc=s96-rw",
      "policies": {
        "Data Categories": 0,
        "Processing Purpose": 1,
        "Data Recipients": 0,
        "Source of Data": 1,
        "Provision Requirement": 1,
        "Data Safeguards": 1,
        "Profiling": 1,
        "Storage Period": 0,
        "Adequacy Decision": 0,
        "Controllers Contact": 1,
        "DPO Contact": 1,
        "Withdraw Consent": 1,
        "Lodge Complaint": 1,
        "Right to Access": 1,
        "Right to Erase": 1,
        "Right to Restrict": 0,
        "Right to Object": 1,
        "Right to Data Portability": 0
      }
    },
    {
      "id": "facebook",
      "name": "Facebook",
      "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Facebook_Logo_%282019%29.png/1200px-Facebook_Logo_%282019%29.png",
      "policies": {
        "Data Categories": 0,
        "Processing Purpose": 1,
        "Data Recipients": 0,
        "Source of Data": 1,
        "Provision Requirement": 1,
        "Data Safeguards": 1,
        "Profiling": 1,
        "Storage Period": 0,
        "Adequacy Decision": 0,
        "Controllers Contact": 1,
        "DPO Contact": 1,
        "Withdraw Consent": 0,
        "Lodge Complaint": 0,
        "Right to Access": 0,
        "Right to Erase": 1,
        "Right to Restrict": 0,
        "Right to Object": 1,
        "Right to Data Portability": 0
      }
    }
  ]))

  const handleFileUpload = (file: File | null): void => {
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        const content = event.target?.result;
        if (typeof content === 'string') {
          const apps = content.split('\n');
          setAppList(apps);
        }
      };
      reader.readAsText(file);
    }
  };

  const handleSubmit = (): void => {
    console.log(appList);

    toggle()

    setAppData(mockdata)
    setTimeout(() =>{navigate("./overview")}, 7000)
  };

  return (
    <>
      <Stack p={20}>
        <section>
          <Title>Check privacy policies by app list</Title>
          <Text>
          This page allows you to upload a list or CSV file containing the package names of the apps you wish to analyze. Our system will process the data and retrieve the respective privacy policies for analysis.
          <br/>
          To use this feature, follow these steps:

          <ol>
          <li>Prepare a list or CSV file with the package names of the apps you want to check. Each package name should be on a separate line in the file.</li>
          <li>Click the "Upload" button to select and upload the file containing the package names.</li>
          <li>Once the file is uploaded, click the "Check policies" button to start the analysis.</li>
          </ol>
        
          Our application will process the provided app list, retrieve the privacy policies for each app, and present you with the results. You will be able to gain insights into the privacy practices of the specified apps.
          <br/>  <br/>
          Note: Please ensure that the uploaded file contains valid package names and follows the required format.
        
          </Text>
        </section>

        <Box pos="relative">
        <LoadingOverlay visible={visible} overlayBlur={2} />

        <Stack>
        <section>
          <FileInput
            placeholder="Upload list of apps as CSV"
            label="Upload list"
            withAsterisk
            onChange={(files) => handleFileUpload(files)}
          />
        </section>

        <Title order={5}>Alternatively, you can insert a list with the package names of the apps</Title>

        <section>
          <Textarea
            placeholder="List of apps"
            label="List of apps"
            withAsterisk
            autosize
            minRows={6}
            onChange={(event) => setAppList(event.currentTarget.value.split('\n'))}
          />
        </section>

        <section>
          <Button color="dark" onClick={handleSubmit}>
            Check policies
          </Button>
        </section>
        </Stack>

        </Box>
      </Stack>
    </>
  );
}
