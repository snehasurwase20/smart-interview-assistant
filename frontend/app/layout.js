import "./globals.css";

export const metadata = {
  title: "AI Interview System",
  description: "AI Interview Project",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}