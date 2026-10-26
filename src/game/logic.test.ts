import test from 'node:test';
import assert from 'node:assert/strict';
import {
  calculateCameraRelativeMovement,
  calculateCompassNav,
  checkCheckpointCollision,
  calculateMiqatProgress,
} from './logic';

test('Camera relative movement: pressing D (Right) moves screen-right', () => {
  // When camera yaw = 0 (looking towards +Z):
  // Screen right is -X in world space.
  const speed = 10;
  const result = calculateCameraRelativeMovement({ forward: 0, right: 1 }, 0, speed);
  assert.ok(result.isMoving, 'Should be moving');
  assert.ok(result.moveX < -0.1, `moveX should be negative for screen right when yaw=0, got ${result.moveX}`);
  assert.ok(Math.abs(result.moveZ) < 0.001, 'moveZ should be near 0');
});

test('Camera relative movement: pressing A (Left) moves screen-left', () => {
  const speed = 10;
  const result = calculateCameraRelativeMovement({ forward: 0, right: -1 }, 0, speed);
  assert.ok(result.isMoving, 'Should be moving');
  assert.ok(result.moveX > 0.1, `moveX should be positive for screen left when yaw=0, got ${result.moveX}`);
  assert.ok(Math.abs(result.moveZ) < 0.001, 'moveZ should be near 0');
});

test('Camera relative movement: pressing W (Forward) moves into screen (+Z when yaw=0)', () => {
  const speed = 10;
  const result = calculateCameraRelativeMovement({ forward: 1, right: 0 }, 0, speed);
  assert.ok(result.isMoving, 'Should be moving');
  assert.ok(Math.abs(result.moveX) < 0.001, 'moveX should be 0');
  assert.ok(result.moveZ > 0.1, 'moveZ should be positive');
});

test('Compass Nav: target directly ahead', () => {
  // Player at (0, 0) facing +Z (rotY = 0)
  // Target at (0, 50)
  const nav = calculateCompassNav(0, 0, 0, 0, 50);
  assert.equal(nav.direction, 'forward');
  assert.ok(nav.label.includes('Maju Lurus'));
});

test('Compass Nav: target directly to the right', () => {
  // When player faces +Z (rotY = 0):
  // Player right arm is at -X.
  // Target at (-30, 0) is to player's right!
  const nav = calculateCompassNav(0, 0, 0, -30, 0);
  assert.equal(nav.direction, 'right');
  assert.ok(nav.label.includes('Sein Kanan'));
});

test('Compass Nav: target directly to the left', () => {
  // When player faces +Z (rotY = 0):
  // Target at (+30, 0) is to player's left!
  const nav = calculateCompassNav(0, 0, 0, 30, 0);
  assert.equal(nav.direction, 'left');
  assert.ok(nav.label.includes('Sein Kiri'));
});

test('Checkpoint Collision: detects arrival when within radius', () => {
  const arrived = checkCheckpointCollision(10, 10, 12, 11, 4.2);
  assert.equal(arrived.arrived, true);

  const far = checkCheckpointCollision(10, 10, 30, 30, 4.2);
  assert.equal(far.arrived, false);
});

test('calculateMiqatProgress: tracks 0 of 4 correctly', () => {
  const res = calculateMiqatProgress({});
  assert.equal(res.completedCount, 0);
  assert.equal(res.percentage, 0);
  assert.equal(res.isComplete, false);
});

test('calculateMiqatProgress: tracks partial progress (2 of 4 = 50%)', () => {
  const res = calculateMiqatProgress({ bersuci: true, ihram: true });
  assert.equal(res.completedCount, 2);
  assert.equal(res.percentage, 50);
  assert.equal(res.isComplete, false);
});

test('calculateMiqatProgress: tracks full completion (4 of 4 = 100%)', () => {
  const res = calculateMiqatProgress({
    bersuci: true,
    ihram: true,
    niat: true,
    talbiyah: true,
  });
  assert.equal(res.completedCount, 4);
  assert.equal(res.percentage, 100);
  assert.equal(res.isComplete, true);
});

