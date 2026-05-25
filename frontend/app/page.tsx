export default function Home() {
  return (
    <main style={{ padding: 32, fontFamily: "sans-serif" }}>
      <h1>It works.</h1>
      <p>Dev deploy smoke test — {new Date().toISOString()}</p>
    </main>
  );
}
