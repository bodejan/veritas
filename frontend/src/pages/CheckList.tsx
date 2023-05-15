import { Button, FileInput, Stack, Text, Textarea, Title } from '@mantine/core';
import { useForm } from '@mantine/form';
import React, { ReactElement, useState } from 'react';

type FormData = {
  category: string;
  numApps: number;
};

type CategoryProps = {};

export default function CheckList(): ReactElement {
  const form = useForm<FormData>({
    initialValues: {
      category: '',
      numApps: 1,
    },
  });

  const { errors, getInputProps } = form;
  const [appList, setAppList] = useState<string[]>([]);

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
    // Perform further processing or API calls with the appList
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
    </>
  );
}
