import { MediaProvider } from "./context/MediaProvider";
import AppNavigation from "./routes/AppNavigation";

function App() {
  return (
    <MediaProvider>
      <AppNavigation />
    </MediaProvider>
  );
}

export default App;
