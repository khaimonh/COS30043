"use client";

import Image from "next/image";
import { useLang } from "@/lib/i18n";
import { Card, CardBody } from "@/components/ui/Card";

const features = ["home.feature1", "home.feature2", "home.feature3"] as const;

export function PreviewSection() {
  const { t } = useLang();

  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-16 sm:px-6 sm:py-20">
      <div className="grid items-center gap-10 lg:grid-cols-2 lg:gap-14">
        <div className="order-2 lg:order-1">
          <Image
            src="/images/dashboard-preview.svg"
            alt={t("home.image2Alt")}
            width={800}
            height={480}
            className="w-full rounded-2xl border border-border"
          />
        </div>
        <div className="order-1 lg:order-2">
          <h2 className="text-2xl font-bold tracking-tight text-foreground sm:text-3xl">
            {t("home.previewTitle")}
          </h2>
          <p className="mt-4 text-base leading-relaxed text-muted">{t("home.previewText")}</p>
          <ul className="mt-8 space-y-4">
            {features.map((key) => (
              <li key={key}>
                <Card className="overflow-hidden">
                  <CardBody className="flex items-start gap-4">
                    <span className="mt-1.5 block h-2 w-2 shrink-0 rounded-full bg-accent" aria-hidden />
                    <div>
                      <p className="font-semibold text-foreground">{t(key)}</p>
                      <p className="mt-1 text-sm leading-relaxed text-muted">
                        {t(`${key}Text`)}
                      </p>
                    </div>
                  </CardBody>
                </Card>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
