"use client";

import { useState, type FormEvent } from "react";
import { useLang } from "@/lib/i18n";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";

export function GreetingForm() {
  const { t, tf } = useLang();
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [name, setName] = useState<string | null>(null);

  const onSubmit = (e: FormEvent) => {
    e.preventDefault();
    const full = `${firstName} ${lastName}`.trim();
    setName(full.length > 0 ? full : null);
  };

  return (
    <form onSubmit={onSubmit} className="space-y-4" noValidate>
      <div className="grid gap-4 sm:grid-cols-2">
        <label className="block">
          <span className="mb-1.5 block text-sm font-medium text-foreground">
            {t("about.firstNameLabel")}
          </span>
          <Input
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            placeholder={t("about.firstNamePlaceholder")}
            autoComplete="given-name"
            name="firstName"
          />
        </label>
        <label className="block">
          <span className="mb-1.5 block text-sm font-medium text-foreground">
            {t("about.lastNameLabel")}
          </span>
          <Input
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            placeholder={t("about.lastNamePlaceholder")}
            autoComplete="family-name"
            name="lastName"
          />
        </label>
      </div>
      <Button type="submit">{t("about.greetButton")}</Button>
      {name !== null ? (
        <p className="rounded-lg border border-accent/40 bg-accent-soft px-4 py-3 text-base font-semibold text-accent-hover">
          {tf("about.welcome", { name })}
        </p>
      ) : null}
    </form>
  );
}
