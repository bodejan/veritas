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

export default function CheckList({setAppData}: CheckListProps): ReactElement {
  const navigate = useNavigate();

  const [visible, { toggle }] = useDisclosure(false);
  
  const form = useForm<FormData>({
    initialValues: {
      category: '',
      numApps: 1,
    },
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
      "image": "https://play.google.com/store/apps/details?id=com.facebook.katana",
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

  const handleFileUpload = (file: File | null) => {
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

  const handleSubmit = () => {
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
            Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor
            invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et
            accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata
            sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur
            sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna
            aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea
            rebum.
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
