"use client";

import { useState } from "react";

export default function Home() {

  const [file, setFile] = useState(null);
  const [role, setRole] = useState("AI/ML Engineer");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const uploadResume = async () => {

    if (!file) {
      alert("Please select a resume first");
      return;
    }

    setLoading(true);
    setError("");

    try {

      const formData = new FormData();

      formData.append("file", file);
      formData.append("role", role);

      const response = await fetch(
  "https://smart-interview-assistant-api-yryb.onrender.com/upload-resume",

      const data = await response.json();

      setResult(data);

    } catch (err) {

      setError("Backend connection failed");

      console.log(err);

    } finally {

      setLoading(false);

    }

  };

  return (

    <div className="max-w-4xl mx-auto p-10">

      <h1 className="text-5xl font-bold mb-10 text-center">
        AI Interview System
      </h1>


      <div className="border rounded-xl p-8 shadow-md">

        <div className="mb-6">

          <label className="block text-lg font-semibold mb-3">
            Upload Resume
          </label>

          <div className="flex items-center gap-4">

            <label
              className="
              bg-blue-600
              text-white
              px-5
              py-3
              rounded-lg
              cursor-pointer
              hover:bg-blue-700
              "
            >

              Choose Resume

              <input
                type="file"
                className="hidden"
                onChange={(e)=>setFile(e.target.files[0])}
              />

            </label>

            <span className="text-gray-700">

              {
                file
                ? file.name
                : "No file selected"
              }

            </span>

          </div>

        </div>


        <select
          value={role}
          onChange={(e)=>setRole(e.target.value)}
          className="
          border
          p-3
          rounded-lg
          mb-5
          w-full
          "
        >

          <option>
            AI/ML Engineer
          </option>

          <option>
            Backend Engineer
          </option>

        </select>


        <button
          onClick={uploadResume}
          className="
          bg-black
          text-white
          px-6
          py-3
          rounded-lg
          hover:bg-gray-800
          "
        >

          {
            loading
            ? "Uploading..."
            : "Upload Resume"
          }

        </button>


        {error && (

          <p className="text-red-500 mt-4">
            {error}
          </p>

        )}

      </div>


      {result && (

        <div className="mt-10 border rounded-xl p-8 shadow-md">

          <h2 className="text-3xl font-bold mb-5">
            Skills
          </h2>

          <ul className="list-disc pl-6 text-lg">

            {result.skills.map(
              (skill,index)=>(

                <li key={index}>
                  {skill}
                </li>

              )
            )}

          </ul>


          <h2 className="text-3xl font-bold mt-10 mb-5">
            Interview Questions
          </h2>

          {

            result.interview_questions.map(
              (question,index)=>(

                <div
                  key={index}
                  className="mb-8"
                >

                  <p className="font-semibold text-xl mb-3">
                    {question}
                  </p>

                  <textarea
                    placeholder="Write your answer here..."
                    className="
                    w-full
                    border
                    p-4
                    rounded-lg
                    "
                    rows="5"
                  />

                </div>

              )
            )

          }

          <button
            className="
            bg-green-600
            text-white
            px-6
            py-3
            rounded-lg
            hover:bg-green-700
            "
          >
            Submit Answers
          </button>

        </div>

      )}

    </div>

  );

}