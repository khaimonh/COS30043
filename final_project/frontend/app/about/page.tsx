"use client";

import { useLang } from "@/lib/i18n";
import { Section } from "@/components/ui/Section";
import { PageHeader } from "@/components/ui/PageHeader";
import { Card, CardBody, CardHeader, CardTitle } from "@/components/ui/Card";
import { GreetingForm } from "@/components/about/GreetingForm";
import { ImagePicker } from "@/components/about/ImagePicker";

export default function About() {
  const { t } = useLang();

  return (
    <main className="flex-1">
      <PageHeader eyebrow={t("brand.name")} title={t("about.title")} />
      <Section className="pb-16 sm:pb-20">
        <p className="max-w-3xl text-base leading-relaxed text-muted sm:text-lg">
          {t("about.paragraph")}
        </p>

        <div className="mt-12 grid gap-6 lg:grid-cols-2">
          <Card className="self-start">
            <CardHeader>
              <CardTitle>{t("about.formTitle")}</CardTitle>
            </CardHeader>
            <CardBody>
              <p className="mb-5 text-sm text-muted">{t("about.welcomeHint")}</p>
              <GreetingForm />
            </CardBody>
          </Card>

          <Card className="self-start">
            <CardHeader>
              <CardTitle>{t("about.sceneTitle")}</CardTitle>
            </CardHeader>
            <CardBody>
              <ImagePicker />
            </CardBody>
          </Card>
        </div>
      </Section>
    </main>
  );
}
