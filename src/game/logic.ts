/**
 * Logic and math helpers for Ibadah Quest 3D
 */

export interface MovementInput {
  forward: number; // -1 to 1
  right: number;   // -1 (left) to 1 (right)
}

export interface MovementResult {
  moveX: number;
  moveZ: number;
  moveAngle: number;
  isMoving: boolean;
}

/**
 * Calculates world-space movement vector from camera-relative input.
 * When yaw = 0, camera is behind the player looking forward along +Z.
 * In this coordinate system, screen right corresponds to -X in world space.
 */
export function calculateCameraRelativeMovement(
  input: MovementInput,
  cameraYaw: number,
  speed: number
): MovementResult {
  const inputLen = Math.hypot(input.forward, input.right);
  if (inputLen < 0.05) {
    return { moveX: 0, moveZ: 0, moveAngle: 0, isMoving: false };
  }

  const normFwd = input.forward / Math.max(inputLen, 1);
  const normRgt = input.right / Math.max(inputLen, 1);

  // Camera forward vector in world X-Z
  const camFwdX = Math.sin(cameraYaw);
  const camFwdZ = Math.cos(cameraYaw);

  // Camera right vector in world X-Z (F x Up, where Up is (0,1,0))
  // (camFwdX, 0, camFwdZ) x (0, 1, 0) = (-camFwdZ, 0, camFwdX)
  const camRgtX = -camFwdZ;
  const camRgtZ = camFwdX;

  const moveX = (camFwdX * normFwd + camRgtX * normRgt) * speed;
  const moveZ = (camFwdZ * normFwd + camRgtZ * normRgt) * speed;
  const moveAngle = Math.atan2(moveX, moveZ);

  return {
    moveX,
    moveZ,
    moveAngle,
    isMoving: true,
  };
}

export type SeinDirection = 'forward' | 'back' | 'right' | 'left' | 'arrived';

export interface CompassNavResult {
  direction: SeinDirection;
  distance: number;
  label: string;
}

/**
 * Calculates turn-by-turn navigation direction (Sein indicator)
 * relative to the player's facing direction.
 */
export function calculateCompassNav(
  playerX: number,
  playerZ: number,
  playerRotY: number,
  targetX: number,
  targetZ: number,
  arriveThreshold = 5.0
): CompassNavResult {
  const dx = targetX - playerX;
  const dz = targetZ - playerZ;
  const dist = Math.hypot(dx, dz);

  if (dist <= arriveThreshold) {
    return {
      direction: 'arrived',
      distance: dist,
      label: `Sampai di Lokasi (${Math.round(dist)}m)`,
    };
  }

  // Player forward unit vector
  const fwdX = Math.sin(playerRotY);
  const fwdZ = Math.cos(playerRotY);

  // Player right unit vector (perpendicular to forward)
  const rgtX = -fwdZ;
  const rgtZ = fwdX;

  // Normalized direction to target
  const tX = dx / dist;
  const tZ = dz / dist;

  const dotFwd = fwdX * tX + fwdZ * tZ;
  const dotRgt = rgtX * tX + rgtZ * tZ;

  if (dotFwd >= 0.7) {
    return {
      direction: 'forward',
      distance: dist,
      label: `Maju Lurus (${Math.round(dist)}m)`,
    };
  }
  if (dotFwd <= -0.7) {
    return {
      direction: 'back',
      distance: dist,
      label: `Putar Balik (${Math.round(dist)}m)`,
    };
  }
  if (dotRgt > 0) {
    return {
      direction: 'right',
      distance: dist,
      label: `Sein Kanan (${Math.round(dist)}m)`,
    };
  }
  return {
    direction: 'left',
    distance: dist,
    label: `Sein Kiri (${Math.round(dist)}m)`,
  };
}

/**
 * Checks if player has collided with / entered a target checkpoint radius.
 */
export function checkCheckpointCollision(
  playerX: number,
  playerZ: number,
  targetX: number,
  targetZ: number,
  radius = 4.2
): { arrived: boolean; distance: number } {
  const dist = Math.hypot(targetX - playerX, targetZ - playerZ);
  return {
    arrived: dist <= radius,
    distance: dist,
  };
}

export interface MiqatStepsState {
  bersuci?: boolean;
  ihram?: boolean;
  niat?: boolean;
  talbiyah?: boolean;
}

export interface MiqatProgressResult {
  completedCount: number;
  totalSteps: number;
  percentage: number;
  isComplete: boolean;
}

/**
 * Calculates Miqat Fiqh checklist progress for the 4 mandated procedures:
 * 1. Cleaning up (mandi/wudhu)
 * 2. Dressing in Ihram
 * 3. The intention (Niat)
 * 4. The Talbiyah chant
 */
export function calculateMiqatProgress(steps: MiqatStepsState): MiqatProgressResult {
  let completedCount = 0;
  if (steps.bersuci) completedCount++;
  if (steps.ihram) completedCount++;
  if (steps.niat) completedCount++;
  if (steps.talbiyah) completedCount++;

  const totalSteps = 4;
  const percentage = Math.round((completedCount / totalSteps) * 100);
  return {
    completedCount,
    totalSteps,
    percentage,
    isComplete: completedCount === totalSteps,
  };
}

