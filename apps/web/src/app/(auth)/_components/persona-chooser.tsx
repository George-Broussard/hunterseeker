import type { Persona } from "@hunterseeker/shared";

const OPTIONS: ReadonlyArray<{ value: Persona; title: string; description: string }> = [
  {
    value: "seeker",
    title: "Seeker",
    description: "I'm looking for a job. Match me to roles I already qualify for.",
  },
  {
    value: "hunter",
    title: "Hunter",
    description: "I'm hiring. Show me ranked candidates for my open roles.",
  },
];

/**
 * One-shot persona choice at signup. Stored as `role` on the account; the data model can
 * grow into "both" later (issue #7), the UI doesn't need to yet.
 */
export function PersonaChooser({ value, error }: { value?: string; error?: string }) {
  return (
    <fieldset className="space-y-2">
      <legend className="mb-1.5 block text-sm font-medium">I am a…</legend>
      <div className="grid grid-cols-2 gap-2">
        {OPTIONS.map((option) => (
          <label
            key={option.value}
            className="flex cursor-pointer flex-col gap-1 rounded-md border border-foreground/20 p-3 text-left transition-colors has-checked:border-foreground has-checked:bg-foreground/5 has-focus-visible:ring-2 has-focus-visible:ring-foreground/20"
          >
            <span className="flex items-center gap-2 text-sm font-medium">
              <input
                type="radio"
                name="role"
                value={option.value}
                defaultChecked={value === option.value}
                className="accent-foreground"
                required
              />
              {option.title}
            </span>
            <span className="text-xs opacity-70">{option.description}</span>
          </label>
        ))}
      </div>
      {error && (
        <p className="text-xs text-red-700 dark:text-red-300" role="alert">
          {error}
        </p>
      )}
    </fieldset>
  );
}
