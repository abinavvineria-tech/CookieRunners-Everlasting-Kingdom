/// <reference types="vitest" />
import { describe, it, expect, beforeEach } from 'vitest';
import { mainAwards, honoraryAwards, timelineEvents } from '../data/awards';

describe('Awards data layer', () => {
  beforeEach(() => {});

  it('contains exactly 3 main awards', () => {
    expect(mainAwards).toHaveLength(3);
  });

  it('first main award is Legend of Cookie Run Kingdom with White Lily', () => {
    expect(mainAwards[0].id).toBe('legend-kingdom');
    expect(mainAwards[0].winner.name).toContain('White Lily');
  });

  it('best double update references Cradle and Digital Circus', () => {
    const award = mainAwards.find((a) => a.id === 'best-double-update');
    expect(award).toBeDefined();
    expect(award?.winner.name).toContain('Cradle');
    expect(award?.winner.name).toContain('Circus');
  });

  it('honorary awards include Golden Heart, Legendary Duo, Eternal Flame', () => {
    expect(honoraryAwards.length).toBeGreaterThanOrEqual(4);
    const ids = honoraryAwards.map((a) => a.id);
    expect(ids).toContain('golden-heart');
    expect(ids).toContain('legendary-duo');
    expect(ids).toContain('eternal-flame');
  });

  it('timeline has 3 verified events including March 11 remembrance', () => {
    expect(timelineEvents).toHaveLength(3);
    const march11 = timelineEvents.find((e) => e.date.includes('March 11'));
    expect(march11).toBeDefined();
    expect(march11?.title).toContain('Remembrance');
  });

  it('no broken artwork placeholders', () => {
    mainAwards.forEach((a) => {
      expect(a.winner.artworkPlaceholder).toBeTruthy();
    });
    honoraryAwards.forEach((a) => {
      expect(a.recognition).toBeTruthy();
    });
  });
});
