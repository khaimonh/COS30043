import { HeroSection } from "@/components/home/HeroSection";
import { StatsBand } from "@/components/home/StatsBand";
import { SpecSheet } from "@/components/home/SpecSheet";
import { PreviewBand } from "@/components/home/PreviewBand";

export default function Home() {
  return (
    <>
      <HeroSection />
      <StatsBand />
      <SpecSheet />
      <PreviewBand />
    </>
  );
}
