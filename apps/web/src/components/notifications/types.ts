/**
 * In-app notification as the UI sees it. Persona-agnostic: the same panel serves the
 * Hunter and Seeker homes. Replace with the generated API type once a notifications
 * endpoint exists (see the follow-up issue linked from NotificationsPanel).
 */
export type NotificationKind = "new_matches" | "application_stage" | "message" | "connection";

export interface Notification {
  id: string;
  kind: NotificationKind;
  text: string;
  /** ISO-8601 timestamp. */
  at: string;
  read: boolean;
}
