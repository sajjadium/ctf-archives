import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BestAnimesComponent } from './best-animes.component';

describe('BestAnimesComponent', () => {
  let component: BestAnimesComponent;
  let fixture: ComponentFixture<BestAnimesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BestAnimesComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BestAnimesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
