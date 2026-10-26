import test from 'node:test';
import assert from 'node:assert/strict';
import {
  calculateCameraRelativeMovement,
  calculateCompassNav,
  checkCheckpointCollision,
  calculateMiqatProgress,
  shuffleChoices,
  resolvePosActivity,
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

test('shuffleChoices preserves correct answer count and reassigns keys A-D', () => {
  const choices = [
    { text: 'A text', correct: true },
    { text: 'B text', correct: false },
    { text: 'C text', correct: false },
    { text: 'D text', correct: false },
  ];
  const shuffled = shuffleChoices(choices);
  assert.equal(shuffled.length, 4);
  assert.equal(shuffled.filter(c => c.correct).length, 1);
  assert.deepEqual(shuffled.map(c => c.key), ['A', 'B', 'C', 'D']);
});

test('resolvePosActivity strictly routes Tawaf at Pos 2/10/13 and Jamarat at Pos 8/12', () => {
  // Pos 2 is always Tawaf in both modes
  assert.equal(resolvePosActivity(2, 'UMRAH'), 'tawaf');
  assert.equal(resolvePosActivity(2, 'HAJI'), 'tawaf');
  // Pos 3 is Sa'i
  assert.equal(resolvePosActivity(3, 'UMRAH'), 'sai');
  assert.equal(resolvePosActivity(3, 'HAJI'), 'sai');
  // Pos 8 is Jamarat
  assert.equal(resolvePosActivity(8, 'HAJI'), 'jamarat');
  // Pos 10 is Tawaf Ifadah
  assert.equal(resolvePosActivity(10, 'HAJI'), 'tawaf');
  // Pos 12 is Jamarat hari tasyrik
  assert.equal(resolvePosActivity(12, 'HAJI'), 'jamarat');
  // Pos 13 is Tawaf Wada
  assert.equal(resolvePosActivity(13, 'HAJI'), 'tawaf');
});


