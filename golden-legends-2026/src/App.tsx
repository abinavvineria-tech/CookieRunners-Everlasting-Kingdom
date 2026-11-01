import Navigation from './components/Navigation';
import Hero from './sections/Hero';
import MainAwards from './sections/MainAwards';
import HonoraryAwards from './sections/HonoraryAwards';
import Timeline from './sections/Timeline';
import About from './sections/About';
import Footer from './sections/Footer';

export default function App() {
  return (
    <div className="min-h-screen bg-midnight text-ivory overflow-x-hidden">
      <Navigation />
      <main>
        <Hero />
        <MainAwards />
        <HonoraryAwards />
        <Timeline />
        <About />
      </main>
      <Footer />
    </div>
  );
}
