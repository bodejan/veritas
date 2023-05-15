import { Button, Grid, Input, NativeSelect, NumberInput, Stack, Text, Title } from '@mantine/core'
import React from 'react'

export default function Category() {
  return (
   <>

          <Stack>
            <section>
              <Title>Check privacy policies by app category</Title>
              <Text>
              Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. 
              </Text>
            </section>

            <section>
            <Grid>
              <Grid.Col xs={12} lg={6}>
              <NativeSelect
                data={['Category1', 'Category2', 'Category3', 'Category4']}
                label="Select category"
                description="Select a category for apps you want to check"
                withAsterisk
              />
              
              </Grid.Col>
              <Grid.Col xs={6} lg={4}>

              <NumberInput
                label="Amount of Apps"
                description="How many apps do you want to analyse?"
                placeholder="0"
                defaultValue={0}
              />
              </Grid.Col>
              <Grid.Col xs={6} lg={2} display="flex" sx={{alignItems: "end"}}>
                <Button color="dark">Check policies</Button>
              </Grid.Col>
            </Grid>
            </section>

            </Stack>

   </>
  )
}
