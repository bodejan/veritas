import { Center, Image, Stack, Text, Title } from '@mantine/core'
import React, { useEffect, useState } from 'react'
import ReactMarkdown from 'react-markdown'

export default function Documentation() {

  const [content, setContent] = useState("");

  useEffect(() => {
    fetch("http://localhost:3000/README.md")
      .then((res) => res.text())
      .then((text) => setContent(text));
  }, []);

  return (
   <>
    <div className="post">
      <ReactMarkdown children={content} />
    </div>
   </>
  )
}
