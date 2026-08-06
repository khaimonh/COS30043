import { HeroSection } from "@/components/home/HeroSection";
import { PreviewSection } from "@/components/home/PreviewSection";

export default function Home() {
  return (
    <main className="flex-1">
      <HeroSection />
      <PreviewSection />
    </main>
  );
}
