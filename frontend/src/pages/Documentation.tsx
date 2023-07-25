import React, { useEffect, useState } from 'react'
import ReactMarkdown from 'react-markdown'


// Component for displaying the README file on the documentation page
export default function Documentation() {

  // Store the data from the README
  const [content, setContent] = useState("");

  // Fetch README from public directory, not from root directory!
  useEffect(() => {
    fetch("http://localhost:3000/README.md")
      .then((res) => res.text())
      .then((text) => setContent(text));
  }, []);

  return (
   <>
    <div className="post">
      {/* Use Markdown parser to parse the README which is stored in "content" */}
      <ReactMarkdown children={content} />
    </div>
   </>
  )
}
