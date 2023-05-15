import { Button, Grid, Input, NativeSelect, NumberInput, Stack, Text, Title } from '@mantine/core'
import { useForm } from '@mantine/form';
import React, { ReactElement } from 'react';

type FormData = {
  category: string;
  numApps: number;
};

type CategoryProps = {};

export default function CheckCategory(props: CategoryProps): ReactElement<CategoryProps> {
  const form = useForm<FormData>({
    initialValues: {
      category: '',
      numApps: 1,
    },

    /*
    validate: {
      category: (value) => (value ? null : 'Invalid category'),
      numApps: (value) => (value < 2 ? null : 'Invalid number of apps'),
    },
*/
  });

  const { errors, getInputProps } = form;

  const handleSubmit = () => {
    if (form.values.category && form.values.numApps >= 1) {
      console.log('Selected category:', form.values.category);
      console.log('Number of apps:', form.values.numApps);
    }
  };

  return (
    <>
      <Stack p={20}>
        <section>
          <Title>Check privacy policies by app category</Title>
          <Text>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. </Text>
        </section>

        <section>
          <Grid>
            <Grid.Col xs={12} lg={6}>
              <NativeSelect
                {...getInputProps('category')}
                data={['Category1', 'Category2', 'Category3', 'Category4']}
                label="Select category"
                description="Select a category for apps you want to check"
                withAsterisk
                required
              />
              {errors.category && <div>{errors.category}</div>}
            </Grid.Col>
            <Grid.Col xs={6} lg={4}>
              <NumberInput
                {...getInputProps('numApps')}
                label="Amount of Apps"
                description="How many apps do you want to analyze?"
                placeholder="1"
                min={1}
                withAsterisk
                required
              />
              {errors.numApps && <div>{errors.numApps}</div>}
            </Grid.Col>
            <Grid.Col xs={6} lg={2} display="flex" sx={{ alignItems: 'end' }}>
              <Button color="dark" onClick={handleSubmit}>
                Check policies
              </Button>
            </Grid.Col>
          </Grid>
        </section>
      </Stack>
    </>
  );
}
